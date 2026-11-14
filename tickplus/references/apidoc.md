# TickPlus API 接口文档

本文由 TickPlus `apidoc.json` 生成，接口名称、参数、返回字段、示例和权限以该文件为准。

- **官方网站**：http://www.tickplus.org
- **API 基址**：http://api.tickplus.org
- **请求方式**：GET

权限代码：1 基础版，2 高级版，3 专业版。

## Basic Api

### 1. 股票列表

获取股票分类列表，包括沪深京A股、ETF基金、沪深可转债、沪深主要指数。

- **路径**：`/plus/basic/list`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：基础数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
| name | String | 股票名称 |

**请求示例**

```text
http://api.tickplus.org/plus/basic/list?symbol=stock&token=123456789
```

**响应示例**

```json
[
  {
    "code": "000011",
    "name": "深物业A"
  },
  {
    "code": "300697",
    "name": "电工合金"
  }
]
```

### 2. 实时行情

股票实时行情数据，更新速度快，适合盯盘。

- **路径**：`/plus/basic/fullquotes`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：行情数据、api全推

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 否 |  | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/basic/fullquotes?symbol=stock&code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 15:30:00",
    "code": "002937",
    "o": 20.15,
    "c": 19.7,
    "h": 20.51,
    "l": 19.6,
    "v": 43719.0,
    "a": 87486200.0,
    "pc": 20.03
  },
  {
    "t": "2026-11-13 15:30:10",
    "code": "603236",
    "o": 85.3,
    "c": 83.0,
    "h": 86.1,
    "l": 82.4,
    "v": 178527.0,
    "a": 1499447600.0,
    "pc": 85.2
  }
]
```

### 3. 日线数据

实时日K线数据，按个股获取日K线数据，包括前复权、后复权、不复权。

- **路径**：`/plus/basic/daykline`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：行情数据、批量

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 是 |  | 股票代码，仅支持单个股票获取 |
| period | String | 是 | 1d-日线，1w-周线，1mon-月线，1y-年线 | K线周期 |
| dividend | String | 是 | 1-不复权，2-前复权，3-后复权 | 复权类型 |
| startDate | String | 是 |  | 开始日期 |
| endDate | String | 是 |  | 结束日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/basic/daykline?symbol=stock&code=000001&period=1d&dividend=1&startDate=2026-11-14&endDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 15:30:00",
    "code": "002937",
    "o": 20.15,
    "c": 19.7,
    "h": 20.51,
    "l": 19.6,
    "v": 43719.0,
    "a": 87486200.0,
    "pc": 20.03
  },
  {
    "t": "2026-11-13 15:30:10",
    "code": "603236",
    "o": 85.3,
    "c": 83.0,
    "h": 86.1,
    "l": 82.4,
    "v": 178527.0,
    "a": 1499447600.0,
    "pc": 85.2
  }
]
```

### 4. 行情指标

行情指标实时数据，包括量比、换手率、市盈率、市净率、总市值、均价、涨幅、涨速等核心指标。

- **路径**：`/plus/basic/fullmetric`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：行情数据、批量

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | String | 否 |  | 股票代码。code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
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
| sjhsl | float | 实际换手率（%） |
| lb | float | 量比 |
| zsz | float | 总市值（元） |
| ltsz | float | 流通市值（元） |
| sjl | float | 市净率（%） |
| jtsyl | float | 市盈率（静） |
| dtsyl | float | 市盈率（动） |
| ttmsyl | float | 市盈率（TTM） |
| zdf05 | float | 5日涨跌幅（%） |
| zdf10 | float | 10日涨幅（%） |
| zdf20 | float | 20日涨幅（%） |

**请求示例**

```text
http://api.tickplus.org/plus/basic/fullmetric?code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "code": "000001",
    "tradeDate": "2026-11-06 11:10:45",
    "zxj": 11.73,
    "open": 11.62,
    "high": 11.74,
    "low": 11.57,
    "cjl": 717944,
    "cje": 838859000,
    "zrspj": 11.64,
    "jj": 11.68,
    "ztj": 12.8,
    "dtj": 10.48,
    "zdf": 0.77,
    "zde": 0.09,
    "zf": 1.46,
    "hsl": 0.37,
    "sjhsl": 21474836,
    "lb": 1.03,
    "zsz": 227631200000,
    "ltsz": 227628840000,
    "sjl": 0.48,
    "jtsyl": 5.34,
    "dtsyl": 4.36,
    "ttmsyl": 5.24,
    "zdf05": 0.77,
    "zdf10": 4.73,
    "zdf20": 1.21
  },
  {
    "code": "000002",
    "tradeDate": "2026-11-06 11:10:45",
    "zxj": 3.27,
    "open": 3.25,
    "high": 3.3,
    "low": 3.23,
    "cjl": 995994,
    "cje": 324884800,
    "zrspj": 3.33,
    "jj": 3.26,
    "ztj": 3.66,
    "dtj": 3,
    "zdf": -1.8,
    "zde": -0.06,
    "zf": 2.1,
    "hsl": 1.03,
    "sjhsl": 21474836,
    "lb": 1.08,
    "zsz": 39013390000,
    "ltsz": 31768410000,
    "sjl": 0.42,
    "jtsyl": -0.44,
    "dtsyl": -1.22,
    "ttmsyl": -0.46,
    "zdf05": 2.51,
    "zdf10": -2.97,
    "zdf20": -19.46
  }
]
```

### 5. 财务指标

核心财务指标，包括ROE、每股净资产、基本每股收益、净资产收益率等核心财务指标。

- **路径**：`/plus/basic/financecore`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：财务数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | String | 是 |  | 股票代码，仅支持单个股票获取，不支持批量参数，不支持ALL参数。 |
| startDate | String | 是 |  | 开始日期 |
| endDate | String | 是 |  | 结束日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
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

**请求示例**

```text
http://api.tickplus.org/plus/basic/financecore?code=000001&startDate=2026-11-14&endDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "code": "000001",
    "reportDate": "2026-06-30",
    "publicDate": "2026-08-15",
    "ocfps": 11.0797,
    "bps": 24.13,
    "basicEps": 1.24,
    "dilutedEps": 1.24,
    "dps": 14.8335,
    "fund": 4.1445,
    "equity": 4.6746,
    "salesProfit": null,
    "revenueInc": 1.7756,
    "profitInc": 3.3213,
    "netProfitM": 3.3213,
    "netProfitA": 2.8199,
    "roe": 4.6872,
    "grossProfit": null,
    "netProfit": 36.3878,
    "prePay": null,
    "salesCash": null,
    "gearRatio": 90.9067,
    "turnover": null
  },
  {
    "code": "000001",
    "reportDate": "2026-09-30",
    "publicDate": "2026-10-24",
    "ocfps": 14.5946,
    "bps": 24.56,
    "basicEps": 1.94,
    "dilutedEps": 1.94,
    "dps": 15.2775,
    "fund": 4.1453,
    "equity": 7.074,
    "salesProfit": null,
    "revenueInc": 2.4159,
    "profitInc": 2.2092,
    "netProfitM": 2.2092,
    "netProfitA": 2.2342,
    "roe": 7.039,
    "grossProfit": null,
    "netProfit": 38.0078,
    "prePay": null,
    "salesCash": null,
    "gearRatio": 90.6474,
    "turnover": null
  }
]
```

### 6. 股本数据

股本表，已上市流通A股等数据

- **路径**：`/plus/basic/capital`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：财务数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | String | 是 |  | 股票代码，仅支持单个股票获取，不支持批量参数，不支持ALL参数。 |
| startDate | String | 是 |  | 开始日期 |
| endDate | String | 是 |  | 结束日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
| reportDate | String | 报告截止日 |
| publicDate | String | 公告日 |
| totalCapital | Float | 总股本 |
| flowCapital | Float | 已上市流通A股 |
| restrictCapital | Float | 限售流通股份 |

**请求示例**

```text
http://api.tickplus.org/plus/basic/capital?code=000001&startDate=2026-11-14&endDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "code": "000001",
    "reportDate": "2026-06-30",
    "publicDate": "2026-08-15",
    "totalCapital": 19405900000,
    "flowCapital": 19405700000,
    "restrictCapital": 0
  },
  {
    "code": "000001",
    "reportDate": "2026-09-30",
    "publicDate": "2026-10-24",
    "totalCapital": 19405900000,
    "flowCapital": 19405700000,
    "restrictCapital": 0
  }
]
```

### 7. 增量数据

盘后增量更新，获取每日全市场日线数据，仅支持最近一周的增量数据。日线数据每日更新，非常快速、方便。

- **路径**：`/plus/basic/updatedaykline`
- **权限**：基础版 (1)、高级版 (2)、专业版 (3)
- **标签**：行情数据、批量

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| dividend | String | 是 | 1-不复权，2-前复权，3-后复权 | 复权类型 |
| tradeDate | String | 是 |  | 交易日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/basic/updatedaykline?symbol=stock&dividend=1&tradeDate=2026-11-14&token=123456789
```


## Pro Api

### 8. 日内分时

日内分时数据，支持获取交易日当天所有的分钟K线数据，盘中实时更新。

- **路径**：`/plus/pro/timekline`
- **权限**：高级版 (2)、专业版 (3)
- **标签**：行情数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 是 |  | 股票代码，仅支持单个股票获取 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/pro/timekline?symbol=stock&code=000001&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 09:15:00",
    "code": "000001",
    "o": 11.81,
    "c": 11.81,
    "h": 11.81,
    "l": 11.81,
    "v": 0,
    "a": 0,
    "pc": 11.79
  },
  {
    "t": "2026-11-13 09:16:00",
    "code": "000001",
    "o": 11.81,
    "c": 11.8,
    "h": 11.81,
    "l": 11.8,
    "v": 0,
    "a": 0,
    "pc": 11.79
  }
]
```

### 9. 题材概念

获取行业板块、概念板块、特色板块下的成分股数据。

- **路径**：`/plus/pro/gncgf`
- **权限**：高级版 (2)、专业版 (3)
- **标签**：基础数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | hy-行业板块，gn-概念板块，ts-特色板块 | 板块划分 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
| name | String | 股票名称 |

**请求示例**

```text
http://api.tickplus.org/plus/pro/gncgf?symbol=hy&token=88888888
```

**响应示例**

```json
[
  {
    "bkname": "高速公路",
    "stocks": [
      "000429",
      "000548",
      "000755",
      "000828",
      "000886",
      "000900",
      "001965",
      "600012",
      "600020",
      "600033",
      "600035",
      "600106",
      "600269",
      "600350",
      "600368",
      "600377",
      "600548",
      "601107",
      "601188",
      "601518"
    ]
  },
  {
    "bkname": "汽车服务",
    "stocks": [
      "000757",
      "300825",
      "301215",
      "600335",
      "600386",
      "600653",
      "600822",
      "920030"
    ]
  }
]
```

### 10. 分钟K线数据

实时分钟K线数据，盘中1分钟实时更新一次。支持按月调取分钟级别K线数据。

- **路径**：`/plus/pro/minutekline`
- **权限**：高级版 (2)、专业版 (3)
- **标签**：分钟数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 是 |  | 股票代码，仅支持单个股票获取 |
| period | String | 是 | 1m-1分钟线，5m-5分钟线，15m-15分钟线，30m-30分钟线，1h-1小时线 | K线周期 |
| dividend | String | 是 | 1-不复权，2-前复权，3-后复权 | 复权类型 |
| startDate | String | 是 |  | 开始日期 |
| endDate | String | 是 |  | 结束日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/pro/minutekline?symbol=stock&code=000001&period=1d&dividend=1&startDate=2026-11-14&endDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-12 10:30:59",
    "code": "000001",
    "o": 11.69,
    "c": 11.75,
    "h": 11.78,
    "l": 11.66,
    "v": 399619,
    "a": 467905540,
    "pc": 11.71
  },
  {
    "t": "2026-11-12 11:30:59",
    "code": "000001",
    "o": 11.74,
    "c": 11.81,
    "h": 11.81,
    "l": 11.73,
    "v": 205660,
    "a": 242275040,
    "pc": 11.75
  },
  {
    "t": "2026-11-12 14:00:59",
    "code": "000001",
    "o": 11.8,
    "c": 11.77,
    "h": 11.82,
    "l": 11.76,
    "v": 183852,
    "a": 216731250,
    "pc": 11.81
  }
]
```

### 11. 盘中分钟K线

交易日当天，实时分钟K线数据全推，盘中1分钟实时更新一次。

- **路径**：`/plus/pro/fullminute`
- **权限**：高级版 (2)、专业版 (3)
- **标签**：分钟数据、api全推、ws推送

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 否 |  | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/pro/fullminute?symbol=stock&code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 15:00:00",
    "code": "000001",
    "o": 12.06,
    "c": 12.07,
    "h": 12.07,
    "l": 12.06,
    "v": 13881,
    "a": 16754176,
    "pc": 12.06
  },
  {
    "t": "2026-11-13 15:00:00",
    "code": "000002",
    "o": 3.06,
    "c": 3.06,
    "h": 3.06,
    "l": 3.06,
    "v": 14819,
    "a": 4534592,
    "pc": 3.06
  }
]
```

### 12. 盘中分钟快照

实时分钟快照数据全推，盘中秒级实时更新。

- **路径**：`/plus/pro/fullminutesnapshot`
- **权限**：高级版 (2)、专业版 (3)
- **标签**：分钟数据、api全推

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 否 |  | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| code | String | 股票代码 |
| o | float | 开盘价（元） |
| c | float | 收盘价（元） |
| h | float | 最高价（元） |
| l | float | 最低价（元） |
| v | float | 成交量（手） |
| a | float | 成交额（元） |
| pc | float | 昨收价（元） |

**请求示例**

```text
http://api.tickplus.org/plus/pro/fullminutesnapshot?symbol=stock&code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 15:00:00",
    "code": "000001",
    "o": 12.06,
    "c": 12.07,
    "h": 12.07,
    "l": 12.06,
    "v": 13881,
    "a": 16754176,
    "pc": 12.06
  },
  {
    "t": "2026-11-13 15:00:00",
    "code": "000002",
    "o": 3.06,
    "c": 3.06,
    "h": 3.06,
    "l": 3.06,
    "v": 14819,
    "a": 4534592,
    "pc": 3.06
  }
]
```


## Expert Api

### 13. 逐笔交易

逐笔交易历史数据，每日盘后更新。

- **路径**：`/plus/expert/transaction`
- **权限**：专业版 (3)
- **标签**：tick数据

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | String | 是 |  | 股票代码，仅支持单个股票获取，不支持批量参数 |
| tradeDate | String | 是 |  | 交易日期 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| t | String | 交易时间 |
| cjj | float | 成交价（元） |
| zd | float | 涨跌额（元） |
| cjl | long | 成交量（手） |
| cje | long | 成交额（元） |
| bs | int | 买卖点，-1主动性卖，1主动性买 |

**请求示例**

```text
http://api.tickplus.org/plus/expert/transaction?code=000001&tradeDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-12 09:15:00",
    "cjj": 11.7,
    "zd": -0.01,
    "cjl": 195,
    "cje": 228150,
    "bs": -1
  },
  {
    "t": "2026-11-12 09:15:09",
    "cjj": 11.72,
    "zd": 0.01,
    "cjl": 913,
    "cje": 1070036,
    "bs": 1
  },
  {
    "t": "2026-11-12 09:15:45",
    "cjj": 11.72,
    "zd": 0.01,
    "cjl": 913,
    "cje": 1070036,
    "bs": 1
  },
  {
    "t": "2026-11-12 09:16:03",
    "cjj": 11.72,
    "zd": 0.01,
    "cjl": 925,
    "cje": 1084100,
    "bs": 1
  }
]
```

### 14. 买卖五档

买卖五档实时数据全推，盘中秒级实时更新。

- **路径**：`/plus/expert/fivelevel`
- **权限**：专业版 (3)
- **标签**：tick数据、api全推、ws推送

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | String | 是 | stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数 | 股票类型 |
| code | String | 否 |  | 股票代码。code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
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

**请求示例**

```text
http://api.tickplus.org/plus/expert/fivelevel?symbol=stock&code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "t": "2026-11-13 15:30:00",
    "code": "000001",
    "p": 12.07,
    "o": 11.76,
    "h": 12.1,
    "l": 11.7,
    "pc": 11.79,
    "a": 2624481800,
    "v": 2189430,
    "bp1": 12.06,
    "bp2": 12.05,
    "bp3": 12.04,
    "bp4": 12.03,
    "bp5": 12.02,
    "bv1": 1576,
    "bv2": 2413,
    "bv3": 2196,
    "bv4": 1769,
    "bv5": 1483,
    "sp1": 12.07,
    "sp2": 12.08,
    "sp3": 12.09,
    "sp4": 12.1,
    "sp5": 12.11,
    "sv1": 7313,
    "sv2": 19648,
    "sv3": 25195,
    "sv4": 47126,
    "sv5": 11300
  },
  {
    "t": "2026-11-13 15:30:00",
    "code": "000002",
    "p": 3.06,
    "o": 3.15,
    "h": 3.15,
    "l": 3.06,
    "pc": 3.14,
    "a": 518616000,
    "v": 1675267,
    "bp1": 3.06,
    "bp2": 3.05,
    "bp3": 3.04,
    "bp4": 3.03,
    "bp5": 3.02,
    "bv1": 20623,
    "bv2": 32508,
    "bv3": 12549,
    "bv4": 10988,
    "bv5": 7822,
    "sp1": 3.07,
    "sp2": 3.08,
    "sp3": 3.09,
    "sp4": 3.1,
    "sp5": 3.11,
    "sv1": 11385,
    "sv2": 9572,
    "sv3": 5232,
    "sv4": 7947,
    "sv5": 8688
  }
]
```

### 15. 集合竞价

获取沪深A股实时竞价快照数据，竞价时间段：09:15-09:25，盘中实时更新，适合短线打板选股。

- **路径**：`/plus/expert/fullbid`
- **权限**：专业版 (3)
- **标签**：竞价数据、api全推、ws推送

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | String | 否 |  | 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
| t | String | 交易时间 |
| p | float | 最新价（元） |
| pc | float | 昨日收盘价（元） |
| zf | float | 竞价涨幅（%） |
| jv | long | 竞价量（手） |
| je | long | 竞价金额（元） |
| nv | long | 未匹配量（手） |
| ne | long | 未匹配金额（元） |
| bs | int | 买卖点，-1未匹配量靠近卖一侧，1未匹配量靠近买一侧 |

**请求示例**

```text
http://api.tickplus.org/plus/expert/fullbid?code=000001,000002&token=123456789
```

**响应示例**

```json
[
  {
    "code": "000001",
    "t": "2026-11-13 09:25:00",
    "p": 11.76,
    "pc": 11.79,
    "zf": -0.25,
    "jv": 4159,
    "je": 4891000,
    "nv": 355,
    "ne": 417480,
    "bs": -1
  },
  {
    "code": "000002",
    "t": "2026-11-13 09:25:00",
    "p": 3.15,
    "pc": 3.14,
    "zf": 0.32,
    "jv": 3816,
    "je": 1202000,
    "nv": 6077,
    "ne": 1914255,
    "bs": -1
  }
]
```

### 16. 异动数据

涨停板数据全推，包含首板股池，一进二，二进三，三进四这些数据，盘中秒级实时更新。

- **路径**：`/plus/expert/fluctuation`
- **权限**：专业版 (3)
- **标签**：异动数据、api全推

**请求参数**

| 参数名 | 类型 | 必填 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| tradeDate | String | 是 |  | 交易日期。如果为交易日当天 |
| token | String | 是 |  | 登录网站获取token |

**返回字段**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | String | 股票代码 |
| time | String | 交易日期 |
| first | String | 首次触及涨停板时间 |
| days | int | 连续涨停天数 |
| pc | float | 昨日收盘价 |
| p | float | 最新价 |
| v | float | 成交量 |
| a | float | 成交额 |
| fbv | float | 封板量 |
| fba | float | 封板资金 |
| update | String | 更新时间 |

**请求示例**

```text
http://api.tickplus.org/plus/expert/fluctuation?tradeDate=2026-11-14&token=123456789
```

**响应示例**

```json
[
  {
    "code": "002578",
    "time": "2026-11-06 00:00:00",
    "first": "2026-11-06 09:25:00",
    "days": 5,
    "pc": 4.55,
    "p": 5.01,
    "v": 1013120,
    "a": 506808300,
    "fbv": 655663,
    "fba": 328487170,
    "update": "2026-11-06 11:29:57"
  },
  {
    "code": "002388",
    "time": "2026-11-06 00:00:00",
    "first": "2026-11-06 10:27:24",
    "days": 3,
    "pc": 6.06,
    "p": 6.67,
    "v": 985204,
    "a": 608766000,
    "fbv": 164633,
    "fba": 109810210,
    "update": "2026-11-06 11:29:42"
  },
  {
    "code": "301697",
    "time": "2026-11-06 00:00:00",
    "first": "2026-11-06 09:34:06",
    "days": 3,
    "pc": 30.5,
    "p": 36.6,
    "v": 172762,
    "a": 608431100,
    "fbv": 33456,
    "fba": 122448950,
    "update": "2026-11-06 11:29:42"
  }
]
```


## Python SDK 方法

| 接口路径 | SDK 方法 |
| --- | --- |
| `/plus/basic/list` | `BasicApi.getStockList` |
| `/plus/basic/fullquotes` | `BasicApi.getFullQuotes` |
| `/plus/basic/daykline` | `BasicApi.getDayKline` |
| `/plus/basic/fullmetric` | `BasicApi.getFullMetric` |
| `/plus/basic/financecore` | `BasicApi.getFinanceCore` |
| `/plus/basic/capital` | `BasicApi.getCapital` |
| `/plus/basic/updatedaykline` | `BasicApi.getUpdateDayKline` |
| `/plus/pro/timekline` | `ProApi.getTimeKline` |
| `/plus/pro/gncgf` | `ProApi.getGncgf` |
| `/plus/pro/minutekline` | `ProApi.getMinuteKline` |
| `/plus/pro/fullminute` | `ProApi.getFullMinute` |
| `/plus/pro/fullminutesnapshot` | `ProApi.getFullMinuteSnapshot` |
| `/plus/expert/transaction` | `ExpertApi.getTransaction` |
| `/plus/expert/fivelevel` | `ExpertApi.getFiveLevel` |
| `/plus/expert/fullbid` | `ExpertApi.getFullBid` |
| `/plus/expert/fluctuation` | `ExpertApi.getFluctuation` |
