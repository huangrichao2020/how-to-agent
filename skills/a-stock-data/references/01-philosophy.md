# A 股数据获取哲学

## 核心原则
- 数据只是原材料，不做投资决策，除非叠加交易宪法框架
- 多数据源降级，本地缓存优先，频控严格
- 2GB 服务器内存约束下，任何全量查询必须分批

## 数据时效性矩阵
| 需求 | 首选 | 降级1 | 降级2 |
|------|------|-------|-------|
| 实时行情(<1min) | 腾讯 qt.gtimg.cn | MX API | Baostock 昨日收盘 |
| 历史K线 | Baostock Parquet | AkShare | 手动下载 |
| 涨停/板块 | 复盘盒子 API | MX API | 问财 |
| 财务/基本面 | Baostock | AkShare | 东财网页 |

## 约束
- MX API: 20次/天/Key，用 key `mkt_3Y4C0TYM4FCc2uTzVYo_G4MFw7KYPyh8CyJ4J1hEzEc`
- 复盘盒子: 请求间隔 ≥5s
- 全市场扫描: 每批 ≤200 只，防 OOM
