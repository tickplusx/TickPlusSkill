import json

from tickplus.scripts.Config import Config
from tickplus.scripts.util import DataUtil


def getStockList(symbol: str, token: str, method: str = "get") -> str:
    """
    获取股票列表。
    历史数据收盘后六点更新。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数，hk-港股，usa-美股
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/list"
    params = {"symbol": symbol, "token": token}
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/list", params, data)
    return data


def getFullQuotes(symbol: str, code: str = "", token: str = "", method: str = "get") -> str:
    """
    实时行情数据全推。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/fullquotes"
    params = {"symbol": symbol, "token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/fullquotes", params, data)
    return data


def getDayKline(symbol: str, code: str, period: str = "1d", dividend: str = "1",
                startDate: str = "", endDate: str = "", token: str = "", method: str = "get") -> str:
    """
    实时日K线数据，按个股获取日K线数据。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param code: 股票代码，仅支持单个股票获取
    :param period: K线周期，1d-日线，1w-周线，1mon-月线，1y-年线
    :param dividend: 复权类型，1-不复权，2-前复权，3-后复权
    :param startDate: 开始日期
    :param endDate: 结束日期
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/daykline"
    params = {
        "symbol": symbol,
        "code": code,
        "period": period,
        "dividend": dividend,
        "token": token
    }
    if startDate:
        params["startDate"] = startDate
    if endDate:
        params["endDate"] = endDate
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/daykline", params, data)
    return data


def getFullIndicator(symbol: str, code: str = "", token: str = "", method: str = "get") -> str:
    """
    实时行情指标全推，1-2分钟更新一次数据。
    
    :param symbol: stock-沪深京A股，etf-ETF基金
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/fullindicator"
    params = {"symbol": symbol, "token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/fullindicator", params, data)
    return data


def getFinanceCore(code: str, startDate: str = "", endDate: str = "", token: str = "", method: str = "get") -> str:
    """
    核心财务指标，包括ROE、每股净资产、基本每股收益、净资产收益率等核心财务指标。
    
    :param code: 股票代码，仅支持单个股票获取
    :param startDate: 开始日期
    :param endDate: 结束日期
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/financecore"
    params = {"code": code, "token": token}
    if startDate:
        params["startDate"] = startDate
    if endDate:
        params["endDate"] = endDate
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/financecore", params, data)
    return data


def getUpdateDayKline(symbol: str, dividend: str = "1", tradeDate: str = "", token: str = "", method: str = "get") -> str:
    """
    盘后增量更新，获取每日全市场日线数据，仅支持最近一周的增量数据。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param dividend: 复权类型，1-不复权，2-前复权，3-后复权
    :param tradeDate: 交易日期
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/basic/updatedaykline"
    params = {"symbol": symbol, "dividend": dividend, "token": token}
    if tradeDate:
        params["tradeDate"] = tradeDate
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/basic/updatedaykline", params, data)
    return data
