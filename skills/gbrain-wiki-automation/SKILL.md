---
name: gbrain-wiki-automation
description: 自动化将 gbrain 页面同步到 Wiki SPA，并自动触发重建。解决 gbrain 页面无法在网页端访问的问题。
version: 1.0.0
author: Hermes Agent
license: Private
yao_category: "知识类"
---

# Gbrain → Wiki SPA 自动化工作流

## 背景
gbrain 数据库中的页面默认不会出现在 `ai10088.com/wiki` 网页上。需要通过脚本同步 Markdown 文件并触发 SPA 重建。

## 核心机制
修改 `~/wiki/helpers/gbrain_sync.py`，在每次同步完成后自动调用 `publish_static_wiki.py`。

## 实施步骤
1. **编辑同步脚本**: 在 `gbrain_sync.py` 的 `sync()` 函数末尾（无论是否有变更）添加：
   ```python
   publish_script = WIKI_DIR / "helpers" / "publish_static_wiki.py"
   if publish_script.exists():
       subprocess.run([sys.executable, str(publish_script)], capture_output=True, text=True)
   ```
2. **安装 CJK 字体**: 确保服务器安装了中文字体，否则网页显示豆腐块。
   ```bash
   yum install -y google-noto-sans-cjk-ttc-fonts wqy-microhei-fonts
   fc-cache -fv
   ```
3. **验证**: 运行 `python3 ~/wiki/helpers/gbrain_sync.py`，检查 `/www/wwwroot/www.ai10088.com/wiki/pages.json` 是否包含新页面。

## 访问地址
格式: `https://www.ai10088.com/wiki/#/page/<slug>`

## 常见坑
- **权限问题**: 确保 Nginx 用户有读取 `~/wiki/gbrain-sync/` 目录的权限。
- **缓存**: 浏览器可能缓存了旧的 `pages.json`，需强制刷新。
- **重复内容**: 不要手动复制 gbrain 页面到 `queries/` 目录，这会导致重复。让 `gbrain_sync.py` 统一管理。