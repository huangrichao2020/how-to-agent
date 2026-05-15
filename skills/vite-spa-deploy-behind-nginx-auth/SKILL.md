---
name: vite-spa-deploy-behind-nginx-auth
category: devops
description: 将 Vite React SPA 部署到带路径前缀和认证拦截的 Nginx 后面。解决 asset 403、API 路径、SPA fallback 等常见问题。
---

# Vite SPA 部署到 Nginx（带路径前缀 + auth）

## 适用场景
- Vite/React SPA 部署在 Nginx 子路径下（如 `/info-hub/`）
- Nginx 根路径 `/` 有认证保护（如 `location /` 的 `return 403` 或 `auth_basic`）
- Nginx 通过 `location ^~ /info-hub/` 提供免认证访问

## 常见坑

### ❌ 问题 1：Asset 加载 403
**现象**：页面加载后，JS/CSS/图片全部返回 403，控制台报错。

**根因**：Vite 默认 `base: '/'`，构建后的 HTML 引用 asset 路径为 `/assets/index-xxx.js`。浏览器请求该路径时，匹配 Nginx 的 `location /` 规则（有 auth/403），被拒绝。

```
<!-- Vite 默认行为，base='/' -->
<script src="/assets/index-xxx.js"></script>
<!-- 浏览器请求 /assets/... → 匹配 location / → 403 -->
```

**修复**：在 `vite.config.ts` 中设置 `base` 为子路径：
```typescript
// vite.config.ts
export default defineConfig({
  base: '/info-hub/',  // 与 Nginx location 前缀一致
  plugins: [react(), tailwindcss()],
})
```
构建后 asset 路径变为 `/info-hub/assets/...`，匹配 `location ^~ /info-hub/` 规则，不受 `location /` 的 auth 限制。

### ❌ 问题 2：API 调用路径不对
**现象**：前端 `fetch('/api/xxx')` 请求 404。

**根因**：生产环境 API 路径为 `/info-hub/api/xxx`，前端直接用 `/api/xxx` 不匹配 Nginx 的任何规则。

**修复**：统一使用带 baseURL 的 API client：
```typescript
// api/client.ts
import axios from 'axios'
const client = axios.create({
  baseURL: '/info-hub/api',  // 与 Nginx location 一致
  timeout: 30000,
})
export default client
```

### ❌ 问题 3：不带末尾斜杠的 403
**现象**：访问 `https://域名/info-hub`（无末尾斜杠）返回 403。

**根因**：Nginx 的 `location ^~ /info-hub/` 规则**要求末尾斜杠**。访问 `/info-hub` 时不匹配该规则，请求落入 `location /`（有 auth/403），被拒绝。

```nginx
# 这个规则匹配 /info-hub/ 但不匹配 /info-hub
location ^~ /info-hub/ {
    alias /www/wwwroot/info-hub/;
    ...
}

# /info-hub 最终匹配这个 → 403
location / {
    if ($cookie_token != "...") { return 403; }
    proxy_pass ...;
}
```

**修复**：添加精确匹配重定向：
```nginx
# 精确匹配 = 优先级最高
location = /info-hub {
    return 301 /info-hub/;
}
```

⚠️ 注意 `location = /info-hub` 使用 `=` 精确匹配，**不带末尾斜杠**，只匹配 `https://域名/info-hub` 这一个路径。

### ⚠️ SPA fallback 配置
Nginx 的 `location ^~` 块中配置 SPA fallback：

```nginx
location ^~ /info-hub/ {
    alias /www/wwwroot/info-hub/;
    index index.html;
    try_files $uri $uri/ /info-hub/index.html;
}
```

注意 `try_files` 的 fallback 路径必须是 `/info-hub/index.html`（带前缀），因为 `alias` 下的内部重定向需要完整 URI。

## 验证清单
```bash
# 1. 检查 asset 路径是否带前缀
curl -s https://你的域名/info-hub/ | grep -o 'src="[^"]*"' | head -3
# 期望输出: src="/info-hub/assets/index-xxx.js"

# 2. 检查所有 asset 是否 200
curl -sf https://你的域名/info-hub/assets/index-xxx.js -o /dev/null -w "%{http_code}"
# 期望: 200

# 3. 检查 API 是否正常
curl -sf https://你的域名/info-hub/api/health | head -5

# 4. 检查 SPA fallback（前端路由刷新）
curl -sf https://你的域名/info-hub/某个前端路由
# 期望返回 index.html 内容，不是 403/404

# 5. 检查不带斜杠的访问（常见 403 陷阱）
curl -sf https://你的域名/info-hub -o /dev/null -w "%{http_code} → %{redirect_url}"
# 期望: 301 → 自动跳转到 /info-hub/，最终 200
```

## 关键教训
- Vite 构建时 `base` 路径必须与 Nginx 的 `location` 前缀**完全一致**
- HTML 中所有 asset 引用（js/css/font/img）都会带上 `base` 前缀
- `location /` 和 `location ^~ /子路径/` 是**两个独立规则**，`^~` 优先级高于普通前缀匹配
- `try_files` 的 fallback 路径必须包含完整前缀，否则 Nginx 内部重定向会匹配错误规则