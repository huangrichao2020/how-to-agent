---
name: info-hub-stock-integration
category: stock
description: 将本地化 A 股数据引擎（Baostock + Parquet）集成到 FastAPI 项目并通过 Nginx 部署。
---
# Info-Hub 股票引擎深度集成与部署

**适用场景**：将本地化 A 股数据引擎（Baostock + Parquet + 定制指标）集成到现有的 FastAPI 项目中，并通过 Nginx 反向代理对外提供服务。

## 核心架构
1. **数据引擎模块** (`backend/services/stock_engine/`):
   - `local_cache.py`: 读取 `/data/historical/*.parquet`，计算指标。
   - `dump_service.py`: 基于 Baostock 的全量/增量更新逻辑。
2. **定制化指标** (硬编码在引擎中):
   - `MA25`: 25 日均线，计算斜率判断趋势（向上=关注）。
   - `MACD`: 固定参数 `(6, 13, 6)`。
   - `VolMA5/60`: 短期与长期成交量均线。
3. **API 路由** (`backend/routers/stock_analysis.py`):
   - `/api/stock/analysis/{symbol}`: 单股指标查询。
   - `/api/stock/scan/ma25-up`: 扫描全市场 25 日线向上的股票。

## 集成步骤
1. **打 Tag**：集成前先给现有仓库打 Tag。
2. **数据共享**：将外部已下载的 `data/historical` 软链到 `backend/data/historical`。
3. **模块植入**：
   - 创建 `stock_engine` 服务。
   - 在 `main.py` 注册路由。
   - 在 `scheduler.py` 注册每日凌晨 02:00 的增量更新任务。

## Nginx 部署模板
将 FastAPI 服务（如 uvicorn）通过 Nginx 路径转发：
- 设置 `location ^~ /info-hub/` 转发至后端端口。
- **注意末尾斜杠**：`proxy_pass` 目标 URL 末尾需加 `/` 以实现路径剥离。
- **支持 SSE**：必须配置 `proxy_buffering off;` 和 `proxy_read_timeout 300s;` 用于 AI 对话的流式输出。

## 关键经验
- **不要试图发布为 PyPI 包**：如果目标是本地部署服务，直接用源码+Nginx 最快。
- **数据软链优于复制**：多个项目共用一套 Parquet 数据时，使用 `ln -s` 避免数据冗余。
- **增量更新设计**：`dump_service` 需支持读取文件最后日期，仅请求 `last_date+1` 到今天的数据，大幅缩短同步时间。
- **全栈子路径部署**：前端 Vite 构建必须加 `--base=/子路径/`；前端 `axios baseURL` 改为 `/子路径/api`；Nginx 需配置两个 location 块（一个处理静态 SPA 的 `try_files` fallback，一个处理 `/api/` 的 SSE 反向代理）。
- **后端路由去重**：在 `main.py` 注册路由时，如果 Router 自带 prefix，`include_router` 就不要再重复添加，否则会导致 404。