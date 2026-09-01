# DemoTickPlusPythonSkill

TickPlus 股票数据 API Python SDK - 提供中国股市、港股、美股的实时行情和历史数据查询服务，支持 REST API 和 WebSocket 实时推送。

## 📋 项目简介

本项目是 TickPlus 平台的 Python SDK 实现，提供了完整的 API 接口调用封装，支持获取：

- **实时行情**: A股、港股、美股的实时报价数据
- **K线数据**: 日线、周线、月线、分钟线等多种周期
- **财务指标**: ROE、每股收益、净资产等核心财务数据
- **高级数据**: 逐笔交易、买卖五档、集合竞价、涨停板等
- **WebSocket 实时推送**: 长连接实时行情推送，支持秒级更新

## ✨ 主要特性

- ✅ 支持 16 个 REST API 接口，覆盖基础、专业、专家三个等级
- ✅ 支持 WebSocket 实时推送，秒级数据更新
- ✅ 完整的数据类型支持：A股、ETF、债券、指数、港股、美股
- ✅ 清晰的权限分级：基础版、高级版、专业版
- ✅ 简洁的 API 设计，易于集成和使用
- ✅ 完善的文档和示例代码
- ✅ 统一的错误处理和日志输出

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

依赖包：
- `requests`: HTTP 请求库
- `websocket-client`: WebSocket 客户端库
- `pandas`: 数据处理（可选）

## 🚀 快速开始

### 1. 配置 Token

在 [TickPlus官网](http://www.tickplus.org) 注册账号并获取 token，然后修改配置文件：

```python
# tickplus/scripts/Config.py
class Config:
    SERVER_URL = "http://api.tickplus.org"
    TOKEN = "your_token_here"  # 替换为你的token
```

### 2. 基本使用

#### REST API 使用

```python
from tickplus.scripts.api import BasicApi, ProApi, ExpertApi
from tickplus.scripts.Config import Config

token = Config.TOKEN

# 获取股票列表
stocks = BasicApi.getStockList(symbol="stock", token=token)
print(f"共 {len(stocks)} 只股票")

# 获取实时行情
quotes = BasicApi.getFullQuotes(
    symbol="stock", 
    code="000001,000002", 
    token=token
)

# 获取日K线数据
from datetime import datetime, timedelta
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

kline = BasicApi.getDayKline(
    symbol="stock",
    code="000001",
    period="1d",
    dividend="1",
    startDate=start_date,
    endDate=end_date,
    token=token
)
```

#### WebSocket 实时推送使用（新增）

```python
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.Config import Config
import time

token = Config.TOKEN
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

### 3. 运行完整测试

#### 测试 REST API

```bash
python tickplus/scripts/StockApiClient.py
```

这将测试所有 16 个 REST API 接口，验证功能是否正常。

#### 测试 WebSocket 实时推送（新增）

```bash
python tickplus/scripts/StockWebSocketClient.py
```

这将测试 WebSocket 连接、订阅、数据接收、取消订阅等功能。

## 📚 API 接口分类

### WebSocket 实时推送（新增）

| 功能 | 说明 | 权限 |
|------|------|------|
| StockWebSocketClient | WebSocket 客户端 | 专业版+ |
| connect() | 建立 WebSocket 连接 | 专业版+ |
| subscribe() | 订阅股票代码 | 专业版+ |
| unsubscribe() | 取消订阅 | 专业版+ |
| disconnect() | 断开连接 | 专业版+ |

**特点**：
- 长连接，服务器主动推送数据
- 秒级数据更新
- 支持文本和二进制数据格式
- 适用于实时性要求高的场景

### Basic Api（基础接口）- 基础版、高级版、专业版可用

| 接口 | 说明 | 权限 |
|------|------|------|
| getStockList | 获取股票列表 | 基础版+ |
| getFullQuotes | 实时行情全推 | 基础版+ |
| getDayKline | 实时日K线数据 | 基础版+ |
| getFullFactor | 行情指标全推 | 基础版+ |
| getFinanceCore | 核心财务指标 | 基础版+ |
| getUpdateDayKline | 盘后增量数据 | 基础版+ |

### Pro Api（专业接口）- 高级版、专业版可用

| 接口 | 说明 | 权限 |
|------|------|------|
| getFullMinute | 实时分钟全推 | 高级版+ |
| getMinuteKline | 实时分钟K线数据 | 高级版+ |
| getTimeKline | 日内分时数据 | 高级版+ |
| getGncgf | 概念成分股 | 高级版+ |

### Expert Api（专家接口）- 专业版可用

| 接口 | 说明 | 权限 |
|------|------|------|
| getTransaction | 逐笔交易数据 | 专业版 |
| getFullBid | 集合竞价全推 | 专业版 |
| getFullFive | 买卖五档全推 | 专业版 |
| getFullBoard | 涨停板全推 | 专业版 |

**权限说明**：
- **基础版 (1)**: 免费注册用户，可访问 Basic Api
- **高级版 (2)**: 付费升级用户，可访问 Basic Api + Pro Api
- **专业版 (3)**: 专业级用户，可访问所有接口
- 权限向下兼容，高级版权限包含基础版，专业版权限包含高级版

## 📖 详细文档

- **API 接口文档**: [tickplus/references/apidoc.md](tickplus/references/apidoc.md)
- **使用技能文档**: [tickplus/SKILL.md](tickplus/SKILL.md)
- **WebSocket 详细文档**: [tickplus/references/websocket.md](tickplus/references/websocket.md)
- **GitHub 项目**: https://github.com/tickplusx/TickPlusSkill
- **在线文档**: http://www.tickplus.org

## 💡 使用示例

### 示例1：批量获取股票行情

```python
# 获取多只股票的实时行情
codes = "000001,000002,600000,600519"  # 平安银行、万科A、浦发银行、贵州茅台
quotes = BasicApi.getFullQuotes(symbol="stock", code=codes, token=token)

for quote in quotes:
    print(f"{quote['code']}: 最新价={quote['c']}, 昨收={quote['pc']}")
```

### 示例2：获取技术指标

```python
# 获取包含30+技术指标的行情数据
indicators = BasicApi.getFullFactor(
    symbol="stock",
    code="000001",
    token=token
)

if indicators:
    data = indicators[0]
    print(f"最新价: {data['zxj']}")
    print(f"涨跌幅: {data['zdf']}%")
    print(f"换手率: {data['hsl']}%")
    print(f"市盈率(TTM): {data['ttmsyl']}")
    print(f"总市值: {data['zsz']}")
```

### 示例3：获取板块成分股

```python
# 获取行业板块列表（需要高级版或专业版权限）
industries = ProApi.getGncgf(symbol="hy", token=token)

for industry in industries:
    print(f"板块: {industry['bkname']}")
    print(f"成分股数量: {len(industry['stocks'])}")
    print(f"成分股: {', '.join(industry['stocks'][:5])}...")  # 显示前5只
```

### 示例4：获取买卖五档

```python
# 获取买卖五档数据（需要专业版权限）
five_level = ExpertApi.getFullFive(code="000001", token=token)

if five_level:
    data = five_level[0]
    print("买盘:")
    for i in range(1, 6):
        print(f"  买{i}: {data[f'bp{i}']} x {data[f'bv{i}]}")
    
    print("卖盘:")
    for i in range(1, 6):
        print(f"  卖{i}: {data[f'sp{i}']} x {data[f'sv{i}]}")
```

### 示例5：WebSocket 实时推送（新增）

**基础用法**：

```python
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.Config import Config
import time

token = Config.TOKEN
ws_url = f"ws://ws.tickplus.org/ws/{token}"

# 创建客户端实例
client = StockWebSocketClient(ws_url)

# 建立连接
if client.connect():
    # 订阅集合竞价和沪深A股
    auth_codes = ["auction", "000001.SZ", "600000.SH"]
    client.subscribe(token, auth_codes)
    
    # 等待接收数据（服务器会主动推送）
    print("Waiting for real-time data...")
    time.sleep(10)
    
    # 取消订阅
    client.unsubscribe(token, auth_codes)
    
    # 断开连接
    client.disconnect()
```

**高级用法**：

关于 WebSocket 的更多高级功能，包括：
- 自定义消息处理
- 错误处理和自动重连
- 数据批处理和过滤
- 性能优化建议
- 常见问题解答

请参考完整文档：[tickplus/references/websocket.md](tickplus/references/websocket.md)

**获取官方示例代码**：

```bash
# 从 GitHub 获取最新示例
git clone https://github.com/tickplusx/TickPlusSkill.git
cd TickPlusSkill

# 运行 WebSocket 测试
python tickplus/scripts/StockWebSocketClient.py
```

## 🔧 项目结构

```
DemoTickPlusPythonSkill/
├── tickplus/
│   ├── scripts/
│   │   ├── api/
│   │   │   ├── BasicApi.py      # 基础API接口（6个）
│   │   │   ├── ProApi.py        # 专业API接口（6个）
│   │   │   └── ExpertApi.py     # 专家API接口（4个）
│   │   ├── util/
│   │   │   └── DataUtil.py      # 工具类
│   │   ├── Config.py            # 配置文件
│   │   ├── StockApiClient.py    # REST API客户端测试类
│   │   └── StockWebSocketClient.py  # WebSocket客户端（新增）
│   ├── references/
│   │   ├── apidoc.json          # 原始API文档
│   │   ├── apidoc.md            # API接口文档
│   │   └── websocket.md         # WebSocket详细文档（新增）
│   └── SKILL.md                 # 使用技能文档
├── requirements.txt             # 依赖包
└── README.md                    # 项目说明
```

## ⚠️ 注意事项

1. **Token 认证**: 所有接口都需要有效的 token，请在官网注册获取
2. **权限等级**: 
   - Basic Api: 基础版、高级版、专业版可用
   - Pro Api: 高级版、专业版可用
   - Expert Api: 仅专业版可用
   - WebSocket: 专业版可用
3. **WebSocket 连接**:
   - WebSocket地址：`ws://ws.tickplus.org/ws/{token}`
   - 支持实时行情推送，数据更新频率为秒级
   - 订阅后服务器会主动推送数据，无需轮询
   - 支持文本和二进制两种数据格式
   - 详细文档：[tickplus/references/websocket.md](tickplus/references/websocket.md)
   - 官方示例：https://github.com/tickplusx/TickPlusSkill
4. **批量限制**: 批量查询最多支持 100 个股票代码
5. **日期格式**: 统一使用 `YYYY-MM-DD` 格式
6. **交易时间**: 
   - A股: 09:30-11:30, 13:00-15:00
   - 港股: 09:30-12:00, 13:00-16:00
   - 集合竞价: 09:15-09:25
7. **性能建议**:
   - 避免频繁全市场数据请求
   - 批量查询优于多次单次查询
   - 缓存常用数据减少 API 调用
   - 对于实时性要求高的场景，优先使用 WebSocket

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供学习和研究使用。

## 🔗 相关链接

- TickPlus 官网: http://www.tickplus.org
- API 文档: http://www.tickplus.org/doc
- GitHub 项目: https://github.com/tickplusx/TickPlusSkill
- WebSocket 文档: [tickplus/references/websocket.md](tickplus/references/websocket.md)

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- Email: tickplus@126.com

---

**最后更新**: 2026-05-15
