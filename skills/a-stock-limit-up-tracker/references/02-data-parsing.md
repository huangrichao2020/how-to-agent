# MX API 数据解析详解

## 端点信息
- URL: `https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen`
- Key: `mkt_3Y4C0TYM4FCc2uTzVYo_G4MFw7KYPyh8CyJ4J1hEzEc`
- 关键词: "A股 今日涨停 非ST 返回代码 名称 行业 连板数 涨跌幅"

## Markdown 表格列位置
返回格式为 Markdown 表格，按管道符 `|` 分割后：
- vals[1] = 代码
- vals[2] = 名称
- vals[5] = 涨跌幅
- vals[10] = 行业
- vals[11] = 连板数
- vals[12] = 封板时间

## 解析陷阱
- "概念"字段常含顿号，会破坏管道符分割
- 务必优先提取"行业"和"连板数"等稳定字段
- ST 股必须先剔除
