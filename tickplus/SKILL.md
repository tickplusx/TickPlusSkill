---
name: tickplus-stock-api
description: 使用 TickPlus 股票数据 API 获取沪深京A股、ETF基金、沪深可转债、指数的实时行情、K线、财务指标等数据，支持 REST API 和 WebSocket 实时推送
---

# TickPlus 股票数据 API 技能

本技能提供访问 TickPlus 平台的 Python SDK，可以获取中国股市（沪深京A股）、ETF基金、沪深可转债、指数的实时行情、历史K线、财务数据等多种金融数据。

接口清单、参数取值、返回字段与权限等级全部以官方 `apidoc.json` 为准，逐接口明细见 [references/apidoc.md](references/apidoc.md)。

## 核心功能

共 16 个 REST 接口，分为 Basic / Pro / Expert 三组。

### 0. WebSocket 实时推送 - 按数据类型权限开通

- **StockWebSocketClient**: WebSocket 实时数据推送客户端
  - 建立 WebSocket 长连接
  - 订阅/取消订阅股票代码或数据类型
  - 接收实时数据（文本和二进制格式）
  - 支持集合竞价、个股 tick、分钟 K 线等多种数据类型

### 1. Basic Api - 基础数据接口（权限 1、2、3）

- **getStockList**: 获取股票列表（stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数）
- **getFullQuotes**: 实时行情（code 为空则全市场全推，逗号分隔批量最多 100 个）
- **getDayKline**: 日K线数据（1d/1w/1mon/1y，仅支持单个股票）
- **getFullMetric**: 行情指标（量比、换手率、市盈率、市净率、总市值等，**无 symbol 参数**）
- **getFinanceCore**: 核心财务指标（ROE、每股收益、每股净资产等，仅支持单个股票）
- **getCapital**: 股本数据（总股本、已上市流通A股、限售流通股份，仅支持单个股票）
- **getUpdateDayKline**: 盘后增量日线数据（全市场，仅支持最近一周）

### 2. Pro Api - 专业数据接口（权限 2、3）

- **getTimeKline**: 日内分时数据（仅支持单个股票）
- **getGncgf**: 题材概念成分股（hy-行业板块，gn-概念板块，ts-特色板块）
- **getMinuteKline**: 分钟K线数据（1m/5m/15m/30m/1h，仅支持单个股票）
- **getFullMinute**: 盘中分钟K线全推（支持 WebSocket 推送）
- **getFullMinuteSnapshot**: 盘中分钟快照全推（秒级更新）

### 3. Expert Api - 专家级数据接口（权限 3）

- **getTransaction**: 逐笔交易数据（单个股票 + 交易日期）
- **getFiveLevel**: 买卖五档实时全推（symbol 必填，支持 WebSocket 推送）
- **getFullBid**: 集合竞价全推（09:15-09:25，**无 symbol 参数**，支持 WebSocket 推送）
- **getFluctuation**: 异动数据（涨停板股池：首板、一进二、二进三、三进四）

## 使用方法

### 前置准备

1. 在 [TickPlus官网](http://www.tickplus.org) 注册账号并获取 token
2. 在项目配置文件中设置 token（`tickplus/scripts/Config.py`）

### WebSocket 实时推送使用示例

**快速开始**：

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
    # 订阅数据（集合竞价 + 个股 tick + 分钟K线）
    auth_codes = ["auction", "000001.SZ", "600000.SH", "minute.hsj"]
    client.subscribe(token, auth_codes)

    # 等待接收数据
    print("Waiting for data...")
    time.sleep(10)

    # 取消订阅
    client.unsubscribe(token, auth_codes)

    # 断开连接
    client.disconnect()
```

**详细说明**：

关于 WebSocket 的完整使用指南，包括：
- 自定义消息处理
- 错误处理和重连机制
- 数据格式详解
- 高级用法（批处理、数据过滤等）
- 常见问题解答

请参考：[references/websocket.md](references/websocket.md)

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

**支持的订阅类型（authCodes）**：

| authCode | 说明 | 对应 REST 接口 |
| --- | --- | --- |
| `000001.SZ` / `600000.SH` | 个股 tick 数据，按个数订阅 | `/plus/basic/fullquotes`、`/plus/expert/fivelevel` |
| `auction` | 沪深京A股集合竞价期间竞价数据 | `/plus/expert/fullbid` |
| `minute.hsj` | 沪深京A股 1 分钟 K 线 | `/plus/pro/fullminute` |
| `minute.index` | 指数 1 分钟 K 线 | `/plus/pro/fullminute` |
| `minute.etf` | ETF 1 分钟 K 线 | `/plus/pro/fullminute` |

支持同时订阅多个代码。

**获取官方示例代码**：

```bash
git clone https://github.com/tickplusx/TickPlusSkill.git
cd TickPlusSkill
python tickplus/scripts/StockWebSocketClient.py
```

更多详细信息请参考：[references/websocket.md](references/websocket.md)

**运行完整测试**：

```bash
python tickplus/scripts/StockWebSocketClient.py
# 等价写法（在项目根目录执行）
python -m tickplus.scripts.StockWebSocketClient
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

# 获取沪深可转债列表
bonds = BasicApi.getStockList(symbol="bond", token=token)

# 获取指数列表
indexes = BasicApi.getStockList(symbol="index", token=token)
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

# 获取全市场实时行情（code 不传，数据量大，谨慎使用）
all_quotes = BasicApi.getFullQuotes(symbol="stock", token=token)

# 返回字段：t-交易时间, code-股票代码, o-开盘价, c-收盘价,
#          h-最高价, l-最低价, v-成交量(手), a-成交额(元), pc-昨收价
```

### 示例3：获取K线数据

```python
from datetime import datetime, timedelta

# 获取日K线数据（仅支持单个股票）
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

# 获取分钟K线数据（仅支持单个股票）
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
# 行情指标接口没有 symbol 参数，只按 code 获取
indicators = BasicApi.getFullMetric(
    code="000001,000002",
    token=token
)

# 返回字段包括：
# zxj-最新价, zdf-涨跌幅, hsl-换手率, lb-量比
# zsz-总市值, ltsz-流通市值, sjl-市净率
# jtsyl-市盈率(静), dtsyl-市盈率(动), ttmsyl-市盈率(TTM)
# zdf05/zdf10/zdf20 - 5日/10日/20日涨跌幅
```

### 示例5：获取财务与股本数据

```python
# 获取核心财务指标（仅支持单个股票）
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

# 获取股本数据（仅支持单个股票）
capital = BasicApi.getCapital(
    code="000001",
    startDate="2025-01-01",
    endDate="2025-12-31",
    token=token
)
# 返回字段：totalCapital-总股本, flowCapital-已上市流通A股, restrictCapital-限售流通股份
```

### 示例6：获取高级数据

```python
# 获取买卖五档数据（symbol 必填）
five_level = ExpertApi.getFiveLevel(
    symbol="stock",
    code="000001,000002",
    token=token
)
# 返回 bp1-bp5(买一到买五价格), bv1-bv5(买一到买五量)
#      sp1-sp5(卖一到卖五价格), sv1-sv5(卖一到卖五量)

# 获取集合竞价数据（09:15-09:25，无 symbol 参数）
bid_data = ExpertApi.getFullBid(
    code="000001",
    token=token
)

# 获取异动数据（涨停板股池）
fluctuation = ExpertApi.getFluctuation(
    tradeDate="2026-11-14",
    token=token
)
# 返回字段：days-连续涨停天数, first-首次触及涨停板时间,
#          fbv-封板量, fba-封板资金, update-更新时间

# 获取逐笔交易数据（仅支持单个股票）
transactions = ExpertApi.getTransaction(
    code="000001",
    tradeDate="2026-11-14",
    token=token
)
```

### 示例7：获取分钟全推与板块成分股

```python
# 盘中分钟K线全推
full_minute = ProApi.getFullMinute(symbol="stock", code="000001,000002", token=token)

# 盘中分钟快照全推（秒级更新）
snapshot = ProApi.getFullMinuteSnapshot(symbol="stock", code="000001,000002", token=token)

# 获取行业板块成分股（高级版及以上）
industry_stocks = ProApi.getGncgf(symbol="hy", token=token)

# 获取概念板块成分股
concept_stocks = ProApi.getGncgf(symbol="gn", token=token)

# 获取特色板块成分股
special_stocks = ProApi.getGncgf(symbol="ts", token=token)
# 注意：该接口返回结构为 [{"bkname": "板块名", "stocks": ["000429", ...]}, ...]
```

## 完整测试示例

运行完整的API测试：

```python
from tickplus.scripts.StockApiClient import StockApiClient

client = StockApiClient()
client.demoForAllApis()  # 测试所有16个REST API接口
```

或直接执行：

```bash
python tickplus/scripts/StockApiClient.py
# 等价写法（在项目根目录执行）
python -m tickplus.scripts.StockApiClient
```

运行 WebSocket 实时推送测试：

```bash
python tickplus/scripts/StockWebSocketClient.py
```

## 参数说明

### 通用参数

- **token**: 必填，从TickPlus官网获取的认证令牌
- **symbol**: 股票类型，取值仅以下 4 种
  - `stock`: 沪深京A股
  - `etf`: ETF基金
  - `bond`: 沪深可转债
  - `index`: 指数
- **code**: 股票代码
  - 空（不传）: 全市场全推（仅 `fullquotes`、`fullmetric`、`fullminute`、`fullminutesnapshot`、`fivelevel`、`fullbid` 支持）
  - `"000001,000002"`: 批量查询，最多 100 个
  - `"000001"`: 单个股票
  - `daykline`、`financecore`、`capital`、`timekline`、`minutekline`、`transaction` 仅支持单个股票

> 注意：`getFullMetric`（行情指标）与 `getFullBid`（集合竞价）**没有 `symbol` 参数**；`getFiveLevel`（买卖五档）的 `symbol` 为必填。

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

### 板块划分参数

`symbol` for gncgf:
- `hy`: 行业板块
- `gn`: 概念板块
- `ts`: 特色板块

## 注意事项

1. **Token认证**: 所有接口都需要有效的token，请在官网注册获取
2. **权限等级**:
   - Basic Api: 基础版 (1)、高级版 (2)、专业版 (3)
   - Pro Api: 高级版 (2)、专业版 (3)
   - Expert Api: 仅专业版 (3)
   - 权限向下兼容：专业版 > 高级版 > 基础版
3. **批量限制**: 批量查询最多支持100个股票代码
4. **WebSocket 连接**:
   - WebSocket地址：`ws://ws.tickplus.org/ws/{token}`
   - 推送权限按数据类型开通：分钟K线推送（`minute.*`）对应高级版及以上；五档、竞价推送对应专业版
   - 订阅后服务器会主动推送数据，无需轮询
   - 支持文本和二进制（gzip/zip 压缩）两种数据格式
   - 需要先建立连接，再发送订阅消息
5. **日期格式**: 统一使用 `YYYY-MM-DD` 格式
6. **交易时间**:
   - A股: 09:30-11:30, 13:00-15:00
   - 集合竞价: 09:15-09:25
7. **数据更新频率**:
   - 实时行情: 秒级更新
   - 行情指标: 1-2分钟更新
   - 盘中分钟K线: 1分钟更新
   - 财务数据: 季度更新
8. **性能建议**:
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

所有REST接口返回的都是JSON格式的列表数据，每个元素是一个字典：

```python
[
    {
        "code": "000001",
        "tradeDate": "2026-11-06 11:10:45",
        "zxj": 11.73,
        "zdf": 0.77,
        ...
    },
    ...
]
```

## 相关资源

- 官方网站: http://www.tickplus.org
- GitHub 项目: https://github.com/tickplusx/TickPlusSkill
- API文档: references/apidoc.md
- WebSocket详细文档: references/websocket.md
- 完整示例: scripts/StockApiClient.py, scripts/StockWebSocketClient.py, scripts/CompleteExampleClient.py
- 文档生成: scripts/generate_apidoc.py
- 配置说明: scripts/Config.py

## 更新日志

- 2026-11-14: 按最新 apidoc.json 全量同步
  - 方法名更正：行情指标改为 `getFullMetric`、买卖五档改为 `getFiveLevel`、涨停板异动改为 `getFluctuation`（旧方法名已废弃）
  - 新增文档：`getCapital`（股本数据）、`getFullMinuteSnapshot`（盘中分钟快照）
  - 标的类型收敛为 stock/etf/bond/index，移除不支持的境外市场说明
  - 修正行情指标、集合竞价、买卖五档的 symbol 参数说明与调用示例
- 2026-05-15: 新增 WebSocket 实时推送功能
  - 添加 StockWebSocketClient 类，支持长连接实时数据推送
  - 支持订阅/取消订阅股票代码
  - 支持集合竞价、沪深A股等多种数据类型
  - 支持文本和二进制两种数据格式
  - 添加完整的测试代码和使用示例
- 2026-04-24: 核对并更新API接口文档
  - Basic Api: 6个接口（修正行情指标接口URL）
  - Pro Api: 6个接口
  - Expert Api: 4个接口
- 2026-04-23: 初始版本，支持16个API接口
