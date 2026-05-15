# A 股数据获取决策树

## 1. 判断市场
- [ ] 是 A 股吗？→ 否：退出，本 skill 不适用
- [ ] 需要 A 股数据吗？→ 是：继续

## 2. 判断数据类型
- [ ] 实时行情？→ 腾讯 API → 失败 → MX API → 失败 → Baostock 昨日收盘
- [ ] 历史K线？→ Baostock Parquet → 失败 → AkShare
- [ ] 涨停/板块？→ 复盘盒子 → 失败 → MX API
- [ ] 财务数据？→ Baostock → 失败 → AkShare

## 3. 判断约束
- [ ] 是否需要全市场扫描？→ 是：分批 ≤200 只
- [ ] 是否在交易时段？→ 否：提醒用户数据为昨日收盘
- [ ] MX API 今日配额是否充足？→ 否：跳过 MX，用备选源

## 4. 加载分析框架（如需要）
- 需要交易分析？→ 加载 `a-stock-market-analysis-framework` 或 `uwillberich`
- 仅需要原始数据？→ 停留在本 skill
