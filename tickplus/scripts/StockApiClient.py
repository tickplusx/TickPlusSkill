from datetime import datetime, timedelta

from tickplus.scripts.Config import Config
from tickplus.scripts.api import BasicApi, ProApi, ExpertApi


class StockApiClient(object):

    def demoForAllApis(self):
        """
        测试所有API接口
        """
        token = Config.TOKEN
        try:
            print("=" * 80)
            print("开始测试所有 TickPlus API 接口")
            print("=" * 80)

            # ========== Basic Api 测试 ==========
            print("\n【Basic Api 测试】")
            print("-" * 80)

            # 1. 股票列表
            print("\n1. 测试 getStockList - 获取股票列表")
            data = BasicApi.getStockList(symbol="stock", token=token)

            # 2. 实时行情全推
            print("\n2. 测试 getFullQuotes - 实时行情全推")
            data = BasicApi.getFullQuotes(symbol="stock", code="000001,000002", token=token)

            # 3. 实时日K线数据
            print("\n3. 测试 getDayKline - 实时日K线数据")
            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            data = BasicApi.getDayKline(
                symbol="stock", code="000001", period="1d", dividend="1",
                startDate=yesterday, endDate=today, token=token
            )

            # 4. 行情指标全推
            print("\n4. 测试 getFullFactor - 行情指标全推")
            data = BasicApi.getFullFactor(symbol="stock", code="000001,000002", token=token)

            # 5. 核心财务指标
            print("\n5. 测试 getFinanceCore - 核心财务指标")
            data = BasicApi.getFinanceCore(code="000001", startDate="2025-01-01", endDate=today, token=token)

            # 6. 盘后增量数据
            print("\n6. 测试 getUpdateDayKline - 盘后增量数据")
            data = BasicApi.getUpdateDayKline(symbol="stock", dividend="1", tradeDate=yesterday, token=token)

            # ========== Pro Api 测试 ==========
            print("\n【Pro Api 测试】")
            print("-" * 80)

            # 7. 实时分钟全推
            print("\n7. 测试 getFullMinute - 实时分钟全推")
            data = ProApi.getFullMinute(symbol="stock", code="000001,000002", token=token)

            # 8. 实时分钟K线数据
            print("\n8. 测试 getMinuteKline - 实时分钟K线数据")
            data = ProApi.getMinuteKline(
                symbol="stock", code="000001", period="1m", dividend="1",
                startDate=yesterday, endDate=today, token=token
            )

            # 9. 日内分时
            print("\n9. 测试 getTimeKline - 日内分时")
            data = ProApi.getTimeKline(symbol="stock", code="000001", token=token)

            # 10. 概念成分股
            print("\n10. 测试 getGncgf - 概念成分股")
            data = ProApi.getGncgf(symbol="hy", token=token)

            # ========== Expert Api 测试 ==========
            print("\n【Expert Api 测试】")
            print("-" * 80)

            # 13. 逐笔交易
            print("\n13. 测试 getTransaction - 逐笔交易")
            data = ExpertApi.getTransaction(code="000001", tradeDate=yesterday, token=token)

            # 14. 集合竞价全推
            print("\n14. 测试 getFullBid - 集合竞价全推")
            data = ExpertApi.getFullBid(code="000001,000002", token=token)

            # 15. 买卖五档全推
            print("\n15. 测试 getFullFive - 买卖五档全推")
            data = ExpertApi.getFullFive(code="000001,000002", token=token)

            # 16. 涨停板全推
            print("\n16. 测试 getFullBoard - 涨停板全推")
            data = ExpertApi.getFullBoard(tradeDate=today, token=token)

            print("\n" + "=" * 80)
            print("所有 API 接口测试完成！")
            print("=" * 80)

        except Exception as e:
            print(f"\n调用失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 创建客户端实例,测试所有API接口
    client = StockApiClient()
    client.demoForAllApis()
