import json

from tickplus.scripts.Config import Config
from tickplus.scripts.util import DataUtil


def getTransaction(code: str, tradeDate: str, token: str = "", method: str = "get") -> str:
    """
    逐笔交易数据。
    
    :param code: 股票代码，仅支持单个股票获取，不支持批量参数
    :param tradeDate: 交易日期
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/expert/transaction"
    params = {"code": code, "tradeDate": tradeDate, "token": token}
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/expert/transaction", params, data)
    return data


def getFullBid(code: str = "", token: str = "", method: str = "get") -> str:
    """
    获取沪深A股实时竞价数据，竞价时间段：09:15-09:25。
    
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/expert/fullbid"
    params = {"token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/expert/fullbid", params, data)
    return data


def getFullFive(code: str = "", token: str = "", method: str = "get") -> str:
    """
    买卖五档实时数据全推。
    
    :param code: 股票代码。code取值为空，则表示全推全市场数据；code取值为000001,000002，则表示批量获取，股票数量最大为100个；code取值为000001，则表示获取单个股票数据。
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/expert/fullfive"
    params = {"token": token}
    if code:
        params["code"] = code
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/expert/fullfive", params, data)
    return data


def getFullBoard(tradeDate: str, token: str = "", method: str = "get") -> str:
    """
    涨停板数据全推。
    
    :param tradeDate: 交易日期。如果为交易日当天
    :param token: 激活Token参考 http://www.tickplus.org/
    :param method: 请求方法，默认get
    :return: JSON格式的字符串数据
    """
    url = Config.SERVER_URL + "/plus/expert/fullboard"
    params = {"tradeDate": tradeDate, "token": token}
    result = DataUtil.request(url, method, params)
    data = json.loads(result)
    DataUtil.printLog("/plus/expert/fullboard", params, data)
    return data
