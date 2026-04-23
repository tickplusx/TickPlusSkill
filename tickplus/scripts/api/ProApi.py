import json

from tickplus.scripts.Config import Config
from tickplus.scripts.util import DataUtil


def getFullMinute(symbol: str, code: str = "", token: str = "", method: str = "get") -> str:
    """
    实时分钟数据全推。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/fullminute"
    params = {"symbol": symbol, "token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/pro/fullminute", params, data)
    return data


def getMinuteKline(symbol: str, code: str, period: str = "1m", dividend: str = "1", 
                   startDate: str = "", endDate: str = "", token: str = "", method: str = "get") -> str:
    """
    实时分钟K线数据。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param code: 股票代码，仅支持单个股票获取
    :param period: K线周期，1m-1分钟线，5m-5分钟线，15m-15分钟线，30m-30分钟线，1h-1小时线
    :param dividend: 复权类型，1-不复权，2-前复权，3-后复权
    :param startDate: 开始日期
    :param endDate: 结束日期
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/minutekline"
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
    DataUtil.printLog("/plus/pro/minutekline", params, data)
    return data


def getTimeKline(symbol: str, code: str, token: str = "", method: str = "get") -> str:
    """
    日内分时数据。
    
    :param symbol: stock-沪深京A股，etf-ETF基金，bond-沪深可转债，index-指数
    :param code: 股票代码，仅支持单个股票获取
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/timekline"
    params = {"symbol": symbol, "code": code, "token": token}
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/pro/timekline", params, data)
    return data


def getGncgf(symbol: str, token: str = "", method: str = "get") -> str:
    """
    获取行业板块、概念板块、特色板块下的成分股数据。
    
    :param symbol: hy-行业板块，gn-概念板块，ts-特色板块
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/gncgf"
    params = {"symbol": symbol, "token": token}
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/pro/gncgf", params, data)
    return data


def getFullHkQuotes(code: str = "", token: str = "", method: str = "get") -> str:
    """
    港股实时行情全推。
    
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/fullhkquotes"
    params = {"token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/pro/fullhkquotes", params, data)
    return data


def getFullUsaQuotes(code: str = "", token: str = "", method: str = "get") -> str:
    """
    美股实时行情全推。
    
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为BABA,BIDU，则表示批量获取，股票数量最大为100个；code取值为BABA，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/pro/fullusaquotes"
    params = {"token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/pro/fullusaquotes", params, data)
    return data
