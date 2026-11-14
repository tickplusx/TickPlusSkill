import json
import os
import sys
import time
import signal
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.Config import Config
from tickplus.scripts.util import DataUtil


class CompleteExampleClient(StockWebSocketClient):
    """完整的 WebSocket 客户端示例"""

    def __init__(self, url):
        super().__init__(url)
        self.message_count = 0
        self.start_time = None
        self.running = True

        # 注册信号处理器以优雅退出
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """处理中断信号"""
        print("\n收到中断信号，正在关闭连接...")
        self.running = False
        self.disconnect()
        sys.exit(0)

    def on_open(self, ws):
        """连接打开回调"""
        super().on_open(ws)
        self.start_time = time.time()
        print("开始订阅股票数据...")

        # 订阅一些示例股票
        token = Config.TOKEN
        auth_codes = ["auction", "minute.hsj", "000001.SZ", "600000.SH"]
        self.subscribe(token, auth_codes)

    def on_message(self, ws, message):
        """消息处理回调"""
        self.message_count += 1

        if isinstance(message, bytes):
            # 处理二进制数据
            try:
                packet = DataUtil.process_data(message)
                current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{current_time}] 收到二进制数据 #{self.message_count}: {str(packet)[:100]}...")

                # 在这里添加您的业务逻辑
                self._process_stock_data(packet)

            except Exception as e:
                print(f"处理二进制数据时出错: {e}")
        else:
            # 处理文本数据
            try:
                data = json.loads(message)
                current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{current_time}] 收到JSON数据 #{self.message_count}: {data}")

            except (json.JSONDecodeError, TypeError):
                print(f"收到文本数据 #{self.message_count}: {message[:100]}...")

    def on_error(self, ws, error):
        """错误回调"""
        super().on_error(ws, error)
        print(f"WebSocket 错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """关闭回调"""
        super().on_close(ws, close_status_code, close_msg)
        if self.start_time:
            duration = time.time() - self.start_time
            print(f"会话持续时间: {duration:.2f} 秒")
            print(f"总共接收消息: {self.message_count} 条")

    def _process_stock_data(self, data):
        """处理股票数据的具体逻辑"""
        # 这里可以实现您的业务逻辑
        # 例如：数据存储、分析、报警等
        pass

    def run(self, duration=60):
        """运行客户端指定时长"""
        print(f"启动 WebSocket 客户端，运行 {duration} 秒...")

        if self.connect():
            print("成功连接到 WebSocket 服务器")

            start_time = time.time()
            query_at = min(5, duration)
            queried = False
            try:
                while self.running and self.connected:
                    elapsed = time.time() - start_time
                    if not queried and elapsed >= query_at:
                        print("查询当前订阅...")
                        self.query_subscribe(Config.TOKEN)
                        queried = True

                    if elapsed >= duration:
                        break
                    time.sleep(min(1, duration - elapsed))
            finally:
                if self.connected:
                    print("取消部分订阅...")
                    self.unsubscribe(Config.TOKEN, ["auction", "600000.SH"])
                print("运行结束，断开连接...")
                self.disconnect()
        else:
            print("无法连接到 WebSocket 服务器")



    # authCodes参数解释
    # 订阅tick数据可取枚举值如下：
    # - 000001.SZ - 订阅股票tick数据，按个数订阅，支持多个股票订阅。
    # - auction - 订阅沪深京A股集合竞价期间竞价数据。
    # - minute.hsj - 订阅沪深京A股一分钟K线数据。
    # - minute.index - 订阅A股指数一分钟K线数据。
    # - minute.etf - 订阅ETF一分钟K线数据。
if __name__ == "__main__":
    """主函数"""
    # 配置
    token = Config.TOKEN
    ws_url = f"ws://ws.tickplus.org/ws/{token}"

    # 创建并运行客户端
    client = CompleteExampleClient(ws_url)
    client.run(30)  # 运行30秒
