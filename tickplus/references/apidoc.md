# TickPlus API 接口文档

TickPlus 是一个提供股票实时数据API接口的平台，提供沪深京A股、ETF基金、可转债、指数、港股、美股等多种金融数据的实时查询服务。

**官方网站**: http://www.tickplus.org  
**API地址**: http://api.tickplus.org

---

## 目录

- [Basic Api - 基础接口](#basic-api---基础接口)
  - [1. 股票列表](#1-股票列表)
  - [2. 实时行情全推](#2-实时行情全推)
  - [3. 实时日K线数据](#3-实时日k线数据)
  - [4. 行情指标全推](#4-行情指标全推)
  - [5. 核心财务指标](#5-核心财务指标)
  - [6. 盘后增量数据](#6-盘后增量数据)
- [Pro Api - 专业接口](#pro-api---专业接口)
  - [7. 实时分钟全推](#7-实时分钟全推)
  - [8. 实时分钟K线数据](#8-实时分钟k线数据)
  - [9. 日内分时](#9-日内分时)
  - [10. 概念成分股](#10-概念成分股)
  - [11. 港股实时行情全推](#11-港股实时行情全推)
  - [12. 美股实时行情全推](#12-美股实时行情全推)
- [Expert Api - 专家接口](#expert-api---专家接口)
  - [13. 逐笔交易](#13-逐笔交易)
  - [14. 集合竞价全推](#14-集合竞价全推)
  - [15. 买卖五档全推](#15-买卖五档全推)
  - [16. 涨停板全推](#16-涨停板全推)

---

## Basic Api - 基础接口

### 1. 股票列表

获取股票分类列表。

**接口地址**: `/plus/basic/list`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数，hk-港股，usa-美股 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 股票代码 |
| name | String | 股票名称 |

**示例**:
```
http://api.tickplus.org/plus/basic/list?symbol=stock&token=123456789
```

**返回示例**:
```json
[
  {"code": "000011", "name": "深物业A"},
  {"code": "300697", "name": "电工合金"}
]
```

---

### 2. 实时行情全推

实时行情数据全推。

**接口地址**: `/plus/basic/fullquotes`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/basic/fullquotes?symbol=stock&code=000001,000002&token=123456789
```

---

### 3. 实时日K线数据

实时日K线数据，按个股获取日K线数据。

**接口地址**: `/plus/basic/daykline`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| code | String | 是 | 股票代码，仅支持单个股票获取 |
| period | String | 是 | K线周期：1d-日线，1w-周线，1mon-月线，1y-年线 |
| dividend | String | 是 | 复权类型：1-不复权，2-前复权，3-后复权 |
| startDate | String | 否 | 开始日期 |
| endDate | String | 否 | 结束日期 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/basic/daykline?symbol=stock&code=000001&period=1d&dividend=1&startDate=2026-04-23&endDate=2026-04-23&token=123456789
```

---

### 4. 行情指标全推

实时行情指标全推，1-2分钟更新一次数据。

**接口地址**: `/plus/basic/fullindicator`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金 |
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 股票代码 |
| name | String | 股票名称 |
| tradeDate | String | 交易时间 |
| zxj | float | 最新价（元） |
| open | float | 开盘价（元） |
| high | float | 最高价（元） |
| low | float | 最低价（元） |
| cjl | float | 成交量（手） |
| cje | float | 成交额（元） |
| zrspj | float | 昨日收盘价（元） |
| jj | float | 均价（元） |
| ztj | float | 涨停价（元） |
| dtj | float | 跌停价（元） |
| zdf | float | 涨跌幅（%） |
| zde | float | 涨跌额（元） |
| zf | float | 振幅（%） |
| hsl | float | 换手率（%） |
| lb | float | 量比 |
| zsz | float | 总市值（元） |
| ltsz | float | 流通市值（元） |
| sjl | float | 市净率（%） |
| wb | float | 委比（%） |
| wp | float | 外盘（手） |
| np | float | 内盘（手） |
| roe | float | ROE |
| zgb | float | 总股本（股） |
| ltgb | float | 流通股本（股） |
| jtsyl | float | 市盈率（静） |
| dtsyl | float | 市盈率（动） |
| ttmsyl | float | 市盈率（TTM） |
| zdf03 | float | 3日涨跌幅（%） |
| zdf05 | float | 5日涨跌幅（%） |
| zdf10 | float | 10日涨幅（%） |
| zdf20 | float | 20日涨幅（%） |
| zdf60 | float | 60日涨幅（%） |
| zdfyear | float | 今年以来涨幅（%） |

**示例**:
```
http://api.tickplus.org/plus/basic/fullindicator?symbol=stock&code=000001,000002&token=123456789
```

---

### 5. 核心财务指标

核心财务指标，包括ROE、每股净资产、基本每股收益、净资产收益率等核心财务指标。

**接口地址**: `/plus/basic/financecore`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 是 | 股票代码，仅支持单个股票获取 |
| startDate | String | 是 | 开始日期 |
| endDate | String | 是 | 结束日期 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 股票代码 |
| reportDate | String | 报告截止日 |
| publicDate | String | 公告日 |
| ocfps | Float | 每股经营活动现金流量 |
| bps | Float | 每股净资产 |
| basicEps | Float | 基本每股收益 |
| dilutedEps | Float | 稀释每股收益 |
| dps | Float | 每股未分配利润 |
| fund | Float | 每股资本公积金 |
| equity | Float | 净资产收益率 |
| salesProfit | Float | 销售毛利率 |
| revenueInc | Float | 主营收入同比增长 |
| profitInc | Float | 净利润同比增长 |
| netProfitM | Float | 归属于母公司所有者的净利润同比增长 |
| netProfitA | Float | 扣非净利润同比增长 |
| roe | Float | 净资产收益率 |
| grossProfit | Float | 毛利率 |
| netProfit | Float | 净利率 |
| prePay | Float | 预收款 |
| salesCash | Float | 销售现金流 |
| gearRatio | Float | 资产负债比率 |
| turnover | Float | 存货周转率 |

**示例**:
```
http://api.tickplus.org/plus/basic/financecore?code=000001&startDate=2026-04-23&endDate=2026-04-23&token=123456789
```

---

### 6. 盘后增量数据

盘后增量更新，获取每日全市场日线数据，仅支持最近一周的增量数据。

**接口地址**: `/plus/basic/updatedaykline`

**请求方式**: GET

**权限等级**: 基础版、高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| dividend | String | 是 | 复权类型：1-不复权，2-前复权，3-后复权 |
| tradeDate | String | 是 | 交易日期 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/basic/updatedaykline?symbol=stock&dividend=1&tradeDate=2026-04-23&token=123456789
```

---

## Pro Api - 专业接口

### 7. 实时分钟全推

实时分钟数据全推。

**接口地址**: `/plus/pro/fullminute`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/pro/fullminute?symbol=stock&code=000001,000002&token=123456789
```

---

### 8. 实时分钟K线数据

实时分钟K线数据。

**接口地址**: `/plus/pro/minutekline`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| code | String | 是 | 股票代码，仅支持单个股票获取 |
| period | String | 是 | K线周期：1m-1分钟线，5m-5分钟线，15m-15分钟线，30m-30分钟线，1h-1小时线 |
| dividend | String | 是 | 复权类型：1-不复权，2-前复权，3-后复权 |
| startDate | String | 否 | 开始日期 |
| endDate | String | 否 | 结束日期 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/pro/minutekline?symbol=stock&code=000001&period=1m&dividend=1&startDate=2026-04-23&endDate=2026-04-23&token=123456789
```

---

### 9. 日内分时

日内分时数据。

**接口地址**: `/plus/pro/timekline`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 股票类型：stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 |
| code | String | 是 | 股票代码，仅支持单个股票获取 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/pro/timekline?symbol=stock&code=000001&token=123456789
```

---

### 10. 概念成分股

获取行业板块、概念板块、特色板块下的成分股数据。

**接口地址**: `/plus/pro/gncgf`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| symbol | String | 是 | 板块划分：hy-行业板块，gn-概念板块，ts-特色板块 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| bkname | String | 板块名称 |
| stocks | Array | 股票代码列表 |

**示例**:
```
http://api.tickplus.org/plus/pro/gncgf?symbol=hy&token=88888888
```

**返回示例**:
```json
[
  {"bkname": "大盘股", "stocks": ["000001", "000002"]}
]
```

---

### 11. 港股实时行情全推

港股实时行情全推。

**接口地址**: `/plus/pro/fullhkquotes`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为00001,00002，则表示批量获取，股票数量最大为100个；code取值为00001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/pro/fullhkquotes?code=00001,00002&token=123456789
```

---

### 12. 美股实时行情全推

美股实时行情全推。

**接口地址**: `/plus/pro/fullusaquotes`

**请求方式**: GET

**权限等级**: 高级版、专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为BABA,BIDU，则表示批量获取，股票数量最大为100个；code取值为BABA，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**示例**:
```
http://api.tickplus.org/plus/pro/fullusaquotes?code=BABA,BIDU&token=123456789
```

---

## Expert Api - 专家接口

### 13. 逐笔交易

逐笔交易数据。

**接口地址**: `/plus/expert/transaction`

**请求方式**: GET

**权限等级**: 专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 是 | 股票代码，仅支持单个股票获取，不支持批量参数 |
| tradeDate | String | 是 | 交易日期 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| cjj | float | 成交价（元） |
| zd | float | 涨跌额（元） |
| cjl | long | 成交量（手） |
| cje | long | 成交额（元） |
| bs | int | 买卖点，-1主动性卖，1主动性买 |

**示例**:
```
http://api.tickplus.org/plus/expert/transaction?code=000001&tradeDate=2026-04-23&token=123456789
```

---

### 14. 集合竞价全推

获取沪深A股实时竞价数据，竞价时间段：09:15-09:25。

**接口地址**: `/plus/expert/fullbid`

**请求方式**: GET

**权限等级**: 专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 股票代码 |
| t | String | 交易时间 |
| p | float | 最新价（元） |
| pc | float | 昨日收盘价（元） |
| zf | float | 竞价涨幅（元） |
| jv | long | 竞价量（手） |
| je | long | 竞价金额（元） |
| nv | long | 未匹配量（手） |
| ne | long | 未匹配金额（元） |
| bs | int | 买卖点，-1未匹配量靠近卖一侧，1未匹配量靠近买一侧 |

**示例**:
```
http://api.tickplus.org/plus/expert/fullbid?code=000001,000002&token=123456789
```

---

### 15. 买卖五档全推

买卖五档实时数据全推。

**接口地址**: `/plus/expert/fullfive`

**请求方式**: GET

**权限等级**: 专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 否 | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| t | String | 交易时间 |
| code | String | 股票代码 |
| p | float | 最新价（元） |
| o | float | 开盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| pc | float | 前收盘价（元） |
| a | float | 成交总额（元） |
| v | float | 成交总量（手） |
| bp1 | float | 买一价（元） |
| bp2 | float | 买二价（元） |
| bp3 | float | 买三价（元） |
| bp4 | float | 买四价（元） |
| bp5 | float | 买五价（元） |
| bv1 | float | 买一量（手） |
| bv2 | float | 买二量（手） |
| bv3 | float | 买三量（手） |
| bv4 | float | 买四量（手） |
| bv5 | float | 买五量（手） |
| sp1 | float | 卖一价（元） |
| sp2 | float | 卖二价（元） |
| sp3 | float | 卖三价（元） |
| sp4 | float | 卖四价（元） |
| sp5 | float | 卖五价（元） |
| sv1 | float | 卖一量（手） |
| sv2 | float | 卖二量（手） |
| sv3 | float | 卖三量（手） |
| sv4 | float | 卖四量（手） |
| sv5 | float | 卖五量（手） |

**示例**:
```
http://api.tickplus.org/plus/expert/fullfive?code=000001,000002&token=123456789
```

---

### 16. 涨停板全推

涨停板数据全推。

**接口地址**: `/plus/expert/fullboard`

**请求方式**: GET

**权限等级**: 专业版

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tradeDate | String | 是 | 交易日期。如果为交易日当天 |
| token | String | 是 | 登录网站获取token |

**返回数据**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 股票代码 |
| time | long | 交易日期 |
| ftime | long | 首次触及涨停板时间 |
| days | int | 连续涨停天数 |
| preClose | float | 昨日收盘价 |
| price | float | 最新价 |
| volume | float | 成交量 |
| amount | float | 成交额 |
| fbvolumn | float | 封板量 |
| fbamount | float | 封板资金 |
| uTime | long | 更新时间 |

**示例**:
```
http://api.tickplus.org/plus/expert/fullboard?tradeDate=2026-04-23&token=123456789
```

---

## 权限说明

根据 apiAuth 字段定义，各接口的访问权限如下：

| 权限等级 | 说明 | 可访问接口 |
|---------|------|-----------|
| **基础版** (1) | 免费注册用户 | Basic Api 全部接口 |
| **高级版** (2) | 付费升级用户 | Basic Api + Pro Api 全部接口 |
| **专业版** (3) | 专业级用户 | 所有接口（Basic + Pro + Expert） |

**注意**: 
- 权限等级向下兼容，即专业版用户可以访问所有接口
- 所有接口都需要提供有效的 token 进行身份认证

## 注意事项

1. **Token认证**: 所有接口都需要提供有效的token参数，请在 [TickPlus官网](http://www.tickplus.org) 注册获取
2. **批量限制**: 部分接口支持批量查询，最多支持100个股票代码
3. **日期格式**: 统一使用 `YYYY-MM-DD` 格式
4. **交易时间**: 
   - A股: 09:30-11:30, 13:00-15:00
   - 港股: 09:30-12:00, 13:00-16:00
   - 集合竞价: 09:15-09:25
5. **数据更新频率**:
   - 实时行情: 秒级更新
   - 行情指标: 1-2分钟更新
   - 财务数据: 季度更新
6. **性能建议**:
   - 避免频繁全市场数据请求
   - 批量查询优于多次单次查询
   - 缓存常用数据减少API调用

## Python SDK 使用示例

```python
from tickplus.scripts.api import BasicApi, ProApi, ExpertApi
from tickplus.scripts.Config import Config

# 配置token
token = Config.TOKEN

# 获取股票列表
stocks = BasicApi.getStockList(symbol="stock", token=token)

# 获取实时行情
quotes = BasicApi.getFullQuotes(symbol="stock", code="000001,000002", token=token)

# 获取日K线数据
kline = BasicApi.getDayKline(
    symbol="stock", 
    code="000001", 
    period="1d", 
    dividend="1",
    startDate="2026-04-01", 
    endDate="2026-04-23", 
    token=token
)
```

---

**最后更新**: 2026-04-23
