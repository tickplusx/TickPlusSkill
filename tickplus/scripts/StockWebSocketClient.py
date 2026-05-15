import json
import os
import sys
import time

from tickplus.scripts.util import DataUtil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import websocket  # pip install websocket-client

from tickplus.scripts.Config import Config

'''
# GitHub: https://github.com/tickplusx/TickPlusSkill
# Home：http://www.tickplus.org/
'''


class StockWebSocketClient(object):

    def __init__(self, url):
        self.url = url  # Enter your websocket URL here
        self.ws = None
        self.connected = False

    def on_open(self):
        print('A new WebSocketApp is opened!')
        self.connected = True
        print(f"Connected to {self.url}")

    def on_message(self, message):
        """处理接收到的消息"""
        # 首先检查是否是二进制数据
        if isinstance(message, bytes):
            # 二进制数据（压缩的股票行情数据）如果需要解析二进制数据，可以在这里添加解析逻辑
            packet = DataUtil.process_data(message)
            print(f"Received data: {packet}")
        else:
            # 处理文本数据
            try:
                data = json.loads(message)
                print(f"Received JSON data: {data}")
            except (json.JSONDecodeError, TypeError):
                print(f"Received text data: {message}")

    def on_error(self, error):
        print(f"Error occurred: {error}")
        self.connected = False

    def on_close(self, close_status_code, close_msg):
        print(f"Connection closed. Code: {close_status_code}, Message: {close_msg}")
        self.connected = False

    def connect(self, timeout=30):
        """建立WebSocket连接
        
        Args:
            timeout: 连接超时时间（秒）
            
        Returns:
            bool: 连接是否成功
        """
        # 禁用websocket的调试模式（设置为True可以看到详细的握手信息）
        websocket.enableTrace(False)

        print(f"Creating WebSocketApp with URL: {self.url}")
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        # 使用线程运行WebSocket，避免阻塞
        import threading
        print("Starting WebSocket thread...")

        def run_websocket():
            print("Inside run_websocket, calling run_forever...")
            self.ws.run_forever()
            print("run_forever exited")

        self.ws_thread = threading.Thread(target=run_websocket)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        print("WebSocket thread started")

        # 等待连接建立
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.connected:
                print("WebSocket connection established successfully")
                return True
            time.sleep(0.2)

        print(f"Failed to establish WebSocket connection within {timeout} seconds")
        return False

    def subscribe(self, token, auth_codes):
        """订阅指定的股票代码或数据类型"""
        if not self.connected or not self.ws:
            print("WebSocket is not connected!")
            return False

        data = json.dumps({
            "token": token,
            "operation": "subscribe",
            "authCodes": auth_codes
        })

        print(f"Sending subscription request: {data}")
        try:
            self.ws.send(data)
            print("Subscription request sent successfully")
            return True
        except Exception as e:
            print(f"Failed to send subscription request: {e}")
            return False

    def unsubscribe(self, token, auth_codes):
        """取消订阅指定的股票代码或数据类型"""
        if not self.connected or not self.ws:
            print("WebSocket is not connected!")
            return False

        data = json.dumps({
            "token": token,
            "operation": "unsubscribe",
            "authCodes": auth_codes
        })

        print(f"Sending unsubscription request: {data}")
        try:
            self.ws.send(data)
            print("Unsubscription request sent successfully")
            return True
        except Exception as e:
            print(f"Failed to send unsubscription request: {e}")
            return False

    def disconnect(self):
        """断开WebSocket连接"""
        if self.ws:
            self.ws.close()
            self.connected = False
            print("WebSocket connection closed")


if __name__ == "__main__":

    token = Config.TOKEN  # 官网获取Token
    auth_codes = ["auction", "000001.SZ", "600000.SH"]  # 订阅集合竞价以及沪深A股行情数据
    ws_url = f"ws://ws.tickplus.org/ws/{token}"  # 创建WebSocket URL

    # 创建客户端实例
    xTickClient = StockWebSocketClient(ws_url)

    # 建立连接
    if xTickClient.connect():
        print("Successfully connected to WebSocket server")

        # 测试订阅功能
        print("\n--- Testing Subscription ---")
        subscribe_result = xTickClient.subscribe(token, auth_codes)
        if subscribe_result:
            print(f"Successfully subscribed to: {auth_codes}")
        else:
            print("Failed to subscribe")

        # 等待一段时间以接收数据
        print("\nWaiting for data (10 seconds)...")
        time.sleep(10)

        # 测试取消订阅功能
        print("\n--- Testing Unsubscription ---")
        unsubscribe_result = xTickClient.unsubscribe(token, auth_codes)
        if unsubscribe_result:
            print(f"Successfully unsubscribed from: {auth_codes}")
        else:
            print("Failed to unsubscribe")

        # 再等待几秒观察是否还有数据
        print("\nWaiting for a few more seconds to verify unsubscription...")
        time.sleep(5)

        # 断开连接
        print("\nDisconnecting from WebSocket server...")
        xTickClient.disconnect()
        print("Test completed!")
    else:
        print("Failed to connect to WebSocket server")
