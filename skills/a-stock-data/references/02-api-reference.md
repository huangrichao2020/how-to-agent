# A 股数据源 API 参考

## 腾讯行情 API
- URL: `https://qt.gtimg.cn/q=sh600000,sz000001`
- 编码: GBK（必须解码为 GBK，UTF-8 会乱码）
- 返回格式: `v_sh600000="1~浦发银行~600000~..."`
- 字段位置: vals[1]=名称, vals[2]=代码, vals[3]=当前价, vals[4]=昨收, vals[5]=开盘, vals[30]=时间

## 复盘盒子 API
- Base: `https://www.fupanhezi.com/api`
- 端点: `/stock/v1/board/zt` (涨停), `/news/list` (消息), `/board/sub` (题材)
- 频控: ≥5s/请求
- 本地缓存: `~/.hermes/data/fupanhezi/fupanhezi.db`

## MX API (东方财富)
- Base: `https://mkapi2.dfcfs.com/finskillshub/api/claw`
- Key: `mkt_3Y4C0TYM4FCc2uTzVYo_G4MFw7KYPyh8CyJ4J1hEzEc`
- 端点: `stock_screen` (涨停板)
- 配额: 20次/天

## Baostock
- 安装: `pip install baostock`
- Parquet 缓存: `/root/info-hub/backend/data/cache/`
- 函数: `query_baostock(code, start_date, end_date)`
