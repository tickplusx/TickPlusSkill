---
name: tickplus-stock-api
description: 使用 TickPlus 股票数据 API 获取实时行情、K线数据、财务指标等金融数据，支持 REST API 和 WebSocket 实时推送
---

# TickPlus 股票数据 API 技能

本技能提供访问 TickPlus 平台的 Python SDK，可以获取中国股市（沪深京A股）、港股、美股的实时行情、历史K线、财务数据等多种金融数据。

## 核心功能

### 0. WebSocket 实时推送（新增）- 专业版可用

- **StockWebSocketClient**: WebSocket 实时行情推送客户端（需要专业版权限）
  - 建立 WebSocket 长连接
  - 订阅/取消订阅股票代码
  - 接收实时行情数据（文本和二进制格式）
  - 支持集合竞价、沪深A股等多种数据类型

### 1. Basic Api - 基础数据接口

- **getStockList**: 获取股票列表（支持A股、ETF、债券、指数、港股、美股）
- **getFullQuotes**: 实时行情全推数据
- **getDayKline**: 实时日K线数据（支持日线、周线、月线、年线）
- **getFullFactor**: 行情指标全推（包含涨跌幅、换手率、市盈率等30+指标）
- **getFinanceCore**: 核心财务指标（ROE、每股收益、净资产等）
- **getUpdateDayKline**: 盘后增量数据更新

### 2. Pro Api - 专业数据接口

- **getFullMinute**: 实时分钟数据全推
- **getMinuteKline**: 实时分钟K线数据（1分钟、5分钟、15分钟、30分钟、1小时）
- **getTimeKline**: 日内分时数据
- **getGncgf**: 概念成分股（行业板块、概念板块、特色板块）
- **getFullHkQuotes**: 港股实时行情全推
- **getFullUsaQuotes**: 美股实时行情全推

### 3. Expert Api - 专家级数据接口

- **getTransaction**: 逐笔交易数据
- **getFullBid**: 集合竞价全推（09:15-09:25）
- **getFullFive**: 买卖五档实时数据
- **getFullBoard**: 涨停板数据全推

## 使用方法

### 前置准备

1. 在 [TickPlus官网](http://www.tickplus.org) 注册账号并获取 token
2. 在项目配置文件中设置 token（`tickplus/scripts/Config.py`）

### WebSocket 实时推送使用示例（新增）

```python
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.Config import Config
import time

# 配置token
token = Config.TOKEN

# 创建WebSocket URL
ws_url = f"ws://ws.tickplus.org/ws/{token}"

# 创建客户端实例
client = StockWebSocketClient(ws_url)

# 建立连接
if client.connect():
    # 订阅股票（支持集合竞价、沪深A股等）
    auth_codes = ["auction", "000001.SZ", "600000.SH"]
    client.subscribe(token, auth_codes)
    
    # 等待接收数据
    print("Waiting for data...")
    time.sleep(10)
    
    # 取消订阅
    client.unsubscribe(token, auth_codes)
    
    # 断开连接
    client.disconnect()
```

**WebSocket 消息格式**：

订阅消息：
```json
{
    "token": "your_token",
    "operation": "subscribe",
    "authCodes": ["auction", "000001.SZ", "600000.SH"]
}
```

取消订阅消息：
```json
{
    "token": "your_token",
    "operation": "unsubscribe",
    "authCodes": ["auction", "000001.SZ", "600000.SH"]
}
```

**支持的订阅类型**：
- `auction`: 集合竞价数据（09:15-09:25）
- `000001.SZ`: 深市股票代码
- `600000.SH`: 沪市股票代码
- 其他股票代码格式类似

**运行完整测试**：
```bash
python tickplus/scripts/StockWebSocketClient.py
```

### 基本调用示例

```python
from tickplus.scripts.api import BasicApi, ProApi, ExpertApi
from tickplus.scripts.Config import Config

# 获取配置的token
token = Config.TOKEN
```

### 示例1：获取股票列表

```python
# 获取沪深京A股列表
stocks = BasicApi.getStockList(symbol="stock", token=token)
print(f"共 {len(stocks)} 只股票")

# 获取ETF基金列表
etfs = BasicApi.getStockList(symbol="etf", token=token)

# 获取港股列表
hk_stocks = BasicApi.getStockList(symbol="hk", token=token)
```

### 示例2：获取实时行情

```python
# 获取单只股票实时行情
quote = BasicApi.getFullQuotes(symbol="stock", code="000001", token=token)

# 批量获取多只股票行情（最多100只）
quotes = BasicApi.getFullQuotes(
    symbol="stock", 
    code="000001,000002,600000", 
    token=token
)

# 获取全市场实时行情（数据量大，谨慎使用）
all_quotes = BasicApi.getFullQuotes(symbol="stock", token=token)
```

### 示例3：获取K线数据

```python
from datetime import datetime, timedelta

# 获取日K线数据
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

kline = BasicApi.getDayKline(
    symbol="stock",
    code="000001",
    period="1d",      # 1d-日线, 1w-周线, 1mon-月线, 1y-年线
    dividend="1",     # 1-不复权, 2-前复权, 3-后复权
    startDate=start_date,
    endDate=end_date,
    token=token
)

# 获取分钟K线数据
minute_kline = ProApi.getMinuteKline(
    symbol="stock",
    code="000001",
    period="5m",      # 1m, 5m, 15m, 30m, 1h
    dividend="1",
    startDate=start_date,
    endDate=end_date,
    token=token
)
```

### 示例4：获取行情指标

```python
# 获取包含30+指标的行情数据
indicators = BasicApi.getFullFactor(
    symbol="stock",
    code="000001,000002",
    token=token
)

# 返回的指标包括：
# zxj-最新价, zdf-涨跌幅, hsl-换手率, lb-量比
# zsz-总市值, sjl-市净率, jtsyl-静态市盈率
# zdf03/zdf05/zdf10/zdf20/zdf60 - 不同周期涨跌幅
```

### 示例5：获取财务数据

```python
# 获取核心财务指标
finance = BasicApi.getFinanceCore(
    code="000001",
    startDate="2025-01-01",
    endDate="2025-12-31",
    token=token
)

# 返回的财务指标包括：
# roe-净资产收益率, bps-每股净资产
# basicEps-基本每股收益, salesProfit-销售毛利率
# gearRatio-资产负债比率等
```

### 示例6：获取港股/美股数据

```python
# 获取港股实时行情
hk_quotes = ProApi.getFullHkQuotes(
    code="00001,00002",  # 汇丰控股、银河娱乐
    token=token
)

# 获取美股实时行情
usa_quotes = ProApi.getFullUsaQuotes(
    code="BABA,BIDU,AAPL",  # 阿里巴巴、百度、苹果
    token=token
)
```

### 示例7：获取高级数据

```python
# 获取买卖五档数据
five_level = ExpertApi.getFullFive(
    code="000001,000002",
    token=token
)
# 返回 bp1-bp5(买一到买五价格), bv1-bv5(买一到买五量)
#       sp1-sp5(卖一到卖五价格), sv1-sv5(卖一到卖五量)

# 获取集合竞价数据（09:15-09:25）
bid_data = ExpertApi.getFullBid(
    code="000001",
    token=token
)

# 获取涨停板数据
board_data = ExpertApi.getFullBoard(
    tradeDate="2026-04-23",
    token=token
)
```

### 示例8：获取板块成分股

```python
# 获取行业板块成分股
industry_stocks = ProApi.getGncgf(symbol="hy", token=token)

# 获取概念板块成分股
concept_stocks = ProApi.getGncgf(symbol="gn", token=token)

# 获取特色板块成分股
special_stocks = ProApi.getGncgf(symbol="ts", token=token)
```

## 完整测试示例

运行完整的API测试：

```python
from tickplus.scripts.StockApiClient import StockApiClient

client = StockApiClient()
client.demoForAllApis()  # 测试所有16个REST API接口
```

运行 WebSocket 实时推送测试：

```bash
python tickplus/scripts/StockWebSocketClient.py
```

## 参数说明

### 通用参数

- **token**: 必填，从TickPlus官网获取的认证令牌
- **symbol**: 股票类型
  - `stock`: 沪深京A股
  - `etf`: ETF基金
  - `bond`: 沪深可转债
  - `index`: 指数
  - `hk`: 港股
  - `usa`: 美股

### K线周期参数

**日线周期** (`period` for daykline):
- `1d`: 日线
- `1w`: 周线
- `1mon`: 月线
- `1y`: 年线

**分钟周期** (`period` for minutekline):
- `1m`: 1分钟线
- `5m`: 5分钟线
- `15m`: 15分钟线
- `30m`: 30分钟线
- `1h`: 1小时线

### 复权类型参数

- `1`: 不复权
- `2`: 前复权
- `3`: 后复权

### 股票代码格式

- 单个股票: `"000001"`
- 批量查询: `"000001,000002,600000"` (最多100个)
- 全市场: 留空或不传该参数

## 注意事项

1. **Token认证**: 所有接口都需要有效的token，请在官网注册获取
2. **权限等级**: 
   - Basic Api: 基础版用户可用
   - Pro Api: 高级版用户可用
   - Expert Api: 专业版用户可用（包含 WebSocket 实时推送）
   - 权限向下兼容：专业版 > 高级版 > 基础版
3. **批量限制**: 批量查询最多支持100个股票代码
4. **WebSocket 连接**（专业版）:
   - WebSocket地址：`ws://ws.tickplus.org/ws/{token}`
   - 支持实时行情推送，数据更新频率为秒级
   - 订阅后服务器会主动推送数据，无需轮询
   - 支持文本和二进制两种数据格式
   - 需要先建立连接，再发送订阅消息
5. **日期格式**: 统一使用 `YYYY-MM-DD` 格式
6. **交易时间**: 
   - A股: 09:30-11:30, 13:00-15:00
   - 港股: 09:30-12:00, 13:00-16:00
   - 集合竞价: 09:15-09:25
6. **数据更新频率**:
   - 实时行情: 秒级更新
   - 行情指标: 1-2分钟更新
   - 财务数据: 季度更新
7. **性能建议**:
   - 避免频繁全市场数据请求
   - 批量查询优于多次单次查询
   - 缓存常用数据减少API调用
   - 对于实时性要求高的场景，优先使用 WebSocket

## 错误处理

```python
try:
    data = BasicApi.getFullQuotes(symbol="stock", code="000001", token=token)
    if isinstance(data, list) and len(data) > 0:
        print(f"成功获取 {len(data)} 条数据")
    else:
        print("未获取到数据")
except Exception as e:
    print(f"API调用失败: {e}")
```

## 数据结构

所有API返回的都是JSON格式的列表数据，每个元素是一个字典：

```python
[
    {
        "code": "000001",
        "name": "平安银行",
        "zxj": 10.96,
        "zdf": -0.18,
        ...
    },
    ...
]
```

## 相关资源

- 官方网站: http://www.tickplus.org
- API文档: references/apidoc.md
- WebSocket使用说明: scripts/WEBSOCKET_README.md
- 完整示例: scripts/StockApiClient.py, scripts/StockWebSocketClient.py
- 配置说明: scripts/Config.py

## 更新日志

- 2026-05-15: 新增 WebSocket 实时推送功能
  - 添加 StockWebSocketClient 类，支持长连接实时数据推送
  - 支持订阅/取消订阅股票代码
  - 支持集合竞价、沪深A股等多种数据类型
  - 支持文本和二进制两种数据格式
  - 添加完整的测试代码和使用示例
- 2026-04-24: 核对并更新API接口文档
  - Basic Api: 6个接口（修正fullfactor接口URL）
  - Pro Api: 6个接口
  - Expert Api: 4个接口
- 2026-04-23: 初始版本，支持16个API接口