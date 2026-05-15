---
name: vite-spa-subpath-deploy
description: Deploy a Vite SPA to an Nginx sub-path (e.g., /info-hub/) without 403/404 errors. Covers base config, API path alignment, and asset prefixing.
category: devops
yao_category: "AI工作"
---

# Vite SPA Sub-path Deployment

When deploying a Vite-based React/Vue SPA to a sub-path on Nginx (e.g., `https://example.com/app/`), three things must align or you'll get 403/404s:

## 1. Vite Config (`vite.config.ts`)

Must set `base` to the sub-path:

```ts
export default defineConfig({
  base: '/app/', // MUST match Nginx location prefix
  plugins: [react()],
})
```

**Pitfall:** If `base` is missing or wrong, `index.html` will request `/assets/...` instead of `/app/assets/...`, hitting Nginx root (which may require auth) → 403.

## 2. API Client Paths

If using Axios with `baseURL`:

```ts
// api/client.ts
const client = axios.create({
  baseURL: '/app/api', // Relative path — respects Vite base
})
```

Then use **relative** paths in calls:
```ts
client.get('/stocks/list') // → /app/api/stocks/list ✅
```

**DO NOT** use absolute paths starting with `/api/`:
```ts
client.get('/api/stocks/list') // → /api/stocks/list ❌ (ignores baseURL)
```

For bare `fetch()`, always prepend the sub-path manually:
```ts
fetch('/app/api/assistant/suggest') // ✅
fetch('/api/assistant/suggest')     // ❌
```

## 3. Nginx Config

```nginx
location ^~ /app/ {
    alias /var/www/app/dist/;
    try_files $uri $uri/ /app/index.html;
}

location ^~ /app/api/ {
    proxy_pass http://backend:8001/;
}
```

## Critical Pitfall: Axios Absolute Path vs baseURL

When using `apiClient.get('/api/xxx')` with `baseURL: '/app/api'`:

```
client.get('/api/xxx')     → /api/xxx         ❌ (ignores baseURL!)
client.get('api/xxx')      → /app/api/api/xxx  ❌ (double /api)
client.get('/xxx')         → /xxx              ❌ (ignores baseURL!)
client.get('xxx')          → /app/api/xxx      ✅
```

Axios treats URLs starting with `/` as **absolute paths from the domain root** — they completely bypass `baseURL`. Only bare names (no leading `/`) get relative resolution.

**Rule of thumb for Vite sub-path deployments:**
- `apiClient.get('stocks/list')` → `baseURL + 'stocks/list'` = ✅
- `fetch('/info-hub/api/assistant/chat')` — explicit full path = ✅
- `apiClient.get('/api/stocks/list')` → bypasses baseURL = ❌
- `fetch('/api/assistant/chat')` → wrong domain = ❌

## Build Artifact Cleanup

After each deploy, old `index-*.js` files from previous builds accumulate. The browser cache can load an old hash → broken page.

```bash
# After cp -r dist/* /deploy-dir/
cd /deploy-dir/assets/
current=$(grep -oP 'index-\w+\.js' ../index.html | head -1)
ls index-*.js | grep -v "$current" | xargs rm -f
```

## Verification Checklist

After build + deploy:
1. Check `dist/index.html`: all `<script src>` and `<link href>` should start with `/app/`.
2. Open browser DevTools → Network tab: no 403/404 on assets or API calls.
3. If 403 on `/app/assets/...`, verify Nginx `alias` or `root` points correctly.
4. Confirm no bare `/api/` calls in deployed JS: `grep -o '"/api/[^"]*"' dist/assets/index-*.js`
5. Clean old build artifacts (see above).
6. Hard-refresh browser (Ctrl+F5) to bypass cache.

## Common Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| 403 on `/assets/...` | `base` missing in vite.config | Add `base: '/app/'` |
| 404 on `/api/xxx` | Axios absolute path ignores baseURL | Use relative paths or fix baseURL |
| 404 on `/app/api/xxx` | Nginx proxy not configured | Add `location ^~ /app/api/` block |
| Blank page after refresh | Nginx missing `try_files` | Add `try_files $uri $uri/ /app/index.html` |
| Unexplained 404s after deploy | Old build files in cache | Clean old index-*.js + hard refresh |
| JS syntax error: unexpected token | Line-number prefix from read_file | Check for `1\|import` patterns in source |