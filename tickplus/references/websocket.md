# TickPlus WebSocket 实时数据接入指南

## 概述

TickPlus 平台提供 WebSocket 实时数据推送服务，允许用户订阅股票行情、集合竞价等实时金融数据。通过 WebSocket 长连接，您可以获得秒级的数据更新，无需频繁轮询 API。

## 前置条件

1. **注册账号**：在 [TickPlus官网](http://www.tickplus.org) 注册并获取 Token
2. **安装依赖**：确保已安装 `websocket-client` 库
   ```bash
   pip install websocket-client
   ```
3. **权限要求**：WebSocket 功能需要专业版权限
4. **获取源码**：如遇问题，可从 GitHub 获取最新示例代码
   - GitHub 项目地址：https://github.com/tickplusx/TickPlusSkill
   - 包含完整的 WebSocket 客户端实现和使用示例

## WebSocket 客户端使用

### 1. 基本连接流程

```python
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.Config import Config
import time

# 配置参数
token = Config.TOKEN  # 从配置文件获取 Token
ws_url = f"ws://ws.tickplus.org/ws/{token}"  # WebSocket 连接地址
# 注意：URL格式为 ws://ws.tickplus.org/ws/{token}，token作为路径参数传递

# 创建客户端实例
client = StockWebSocketClient(ws_url)

# 建立连接
if client.connect():
    print("成功连接到 WebSocket 服务器")
    
    # 订阅数据
    auth_codes = ["auction", "000001.SZ", "600000.SH"]
    client.subscribe(token, auth_codes)
    
    # 等待接收数据
    print("等待接收数据...")
    time.sleep(10)
    
    # 取消订阅
    client.unsubscribe(token, auth_codes)
    
    # 断开连接
    client.disconnect()
else:
    print("连接失败")
```

### 2. 自定义消息处理

您可以继承 `StockWebSocketClient` 类并重写 `on_message` 方法来自定义数据处理逻辑：

```python
import json
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient
from tickplus.scripts.util import DataUtil

class CustomWebSocketClient(StockWebSocketClient):
    def on_message(self, message):
        """自定义消息处理"""
        if isinstance(message, bytes):
            # 处理二进制数据（压缩的股票行情）
            packet = DataUtil.process_data(message)
            print(f"收到二进制数据: {packet}")
            
            # 在这里添加您的业务逻辑
            self.process_stock_data(packet)
        else:
            # 处理文本数据
            try:
                data = json.loads(message)
                print(f"收到JSON数据: {data}")
                
                # 在这里添加您的业务逻辑
                self.process_json_data(data)
            except (json.JSONDecodeError, TypeError):
                print(f"收到文本数据: {message}")
    
    def process_stock_data(self, data):
        """处理股票行情数据"""
        # 实现您的数据处理逻辑
        pass
    
    def process_json_data(self, data):
        """处理JSON格式数据"""
        # 实现您的数据处理逻辑
        pass

# 使用自定义客户端
client = CustomWebSocketClient(ws_url)
if client.connect():
    # 订阅并接收数据
    pass
```

### 3. 错误处理和重连机制（扩展示例）

> **注意**：以下重连机制为扩展示例，非源代码直接提供的功能。
> 如需获取官方完整实现，请访问：https://github.com/tickplusx/TickPlusSkill

```python
import time
from tickplus.scripts.StockWebSocketClient import StockWebSocketClient

class RobustWebSocketClient(StockWebSocketClient):
    def __init__(self, url, max_retries=3, retry_delay=5):
        super().__init__(url)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.reconnect_count = 0
    
    def on_error(self, error):
        """错误处理"""
        print(f"发生错误: {error}")
        self.connected = False
        
        # 尝试重连
        if self.reconnect_count < self.max_retries:
            self.reconnect_count += 1
            print(f"尝试第 {self.reconnect_count} 次重连...")
            time.sleep(self.retry_delay)
            self.connect()
        else:
            print("达到最大重连次数，停止重连")
    
    def on_close(self, close_status_code, close_msg):
        """连接关闭处理"""
        print(f"连接关闭. 代码: {close_status_code}, 消息: {close_msg}")
        self.connected = False
        
        # 如果不是主动断开，则尝试重连
        if self.reconnect_count < self.max_retries:
            self.reconnect_count += 1
            print(f"尝试第 {self.reconnect_count} 次重连...")
            time.sleep(self.retry_delay)
            self.connect()

# 使用增强版客户端
client = RobustWebSocketClient(ws_url, max_retries=5, retry_delay=3)
```

## 订阅管理

### 支持的订阅类型

| 类型 | 说明 | 示例 |
|------|------|------|
| auction | 集合竞价数据（09:15-09:25） | `"auction"` |
| 深市股票 | 深圳证券交易所股票 | `"000001.SZ"` |
| 沪市股票 | 上海证券交易所股票 | `"600000.SH"` |

**注意**：股票代码格式为 `{代码}.{市场}`，例如：
- 深市：`000001.SZ`, `000002.SZ`
- 沪市：`600000.SH`, `600001.SH`
- 具体支持的股票代码请参考官方文档或使用 `BasicApi.getStockList()` 获取

### 订阅操作

```python
# 订阅单只股票
client.subscribe(token, ["000001.SZ"])

# 订阅多只股票
client.subscribe(token, ["000001.SZ", "600000.SH", "000002.SZ"])

# 订阅集合竞价数据
client.subscribe(token, ["auction"])

# 混合订阅
client.subscribe(token, ["auction", "000001.SZ", "600000.SH"])

# 取消订阅
client.unsubscribe(token, ["000001.SZ"])
```

### 动态订阅管理

```python
class DynamicSubscriptionManager:
    def __init__(self, ws_client, token):
        self.client = ws_client
        self.token = token
        self.subscribed_codes = set()
    
    def add_subscription(self, codes):
        """添加订阅"""
        new_codes = [code for code in codes if code not in self.subscribed_codes]
        if new_codes:
            self.client.subscribe(self.token, new_codes)
            self.subscribed_codes.update(new_codes)
            print(f"新增订阅: {new_codes}")
    
    def remove_subscription(self, codes):
        """移除订阅"""
        existing_codes = [code for code in codes if code in self.subscribed_codes]
        if existing_codes:
            self.client.unsubscribe(self.token, existing_codes)
            self.subscribed_codes -= set(existing_codes)
            print(f"取消订阅: {existing_codes}")
    
    def get_current_subscriptions(self):
        """获取当前订阅列表"""
        return list(self.subscribed_codes)

# 使用示例
manager = DynamicSubscriptionManager(client, token)
manager.add_subscription(["000001.SZ", "600000.SH"])
manager.remove_subscription(["000001.SZ"])
```

## 数据格式说明

### 接收的数据类型

WebSocket 客户端可以接收两种类型的数据：

1. **文本数据**：JSON 格式的元数据或控制信息
2. **二进制数据**：压缩的股票行情数据（gzip 或 zip 格式）

### 数据处理流程

```python
def on_message(self, message):
    if isinstance(message, bytes):
        # 二进制数据 - 通常是压缩的股票行情
        packet = DataUtil.process_data(message)
        # packet 是解压后的 JSON 数据
    else:
        # 文本数据 - 可能是 JSON 或纯文本
        try:
            data = json.loads(message)
            # 处理 JSON 数据
        except:
            # 处理纯文本数据
            pass
```

### 典型数据结构

股票行情数据通常包含以下字段：
- `code`: 股票代码
- `name`: 股票名称
- `zxj`: 最新价
- `zdf`: 涨跌幅
- `hsl`: 换手率
- `lb`: 量比
- `zsz`: 总市值
- 等其他行情指标

## 高级用法

> **说明**：以下高级用法为扩展示例，展示了如何基于 StockWebSocketClient 进行功能扩展。
> 如需获取官方完整实现和更多示例，请访问：https://github.com/tickplusx/TickPlusSkill

### 1. 数据缓存和批处理（扩展示例）

```python
import queue
import threading
from collections import defaultdict

class BatchDataProcessor:
    def __init__(self):
        self.data_queue = queue.Queue()
        self.batch_size = 100
        self.batch_timeout = 5  # 秒
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_batch)
        self.processor_thread.daemon = True
        self.processor_thread.start()
    
    def add_data(self, data):
        """添加数据到队列"""
        self.data_queue.put(data)
    
    def _process_batch(self):
        """批量处理数据"""
        batch = []
        last_process_time = time.time()
        
        while self.running:
            try:
                # 非阻塞获取数据
                data = self.data_queue.get_nowait()
                batch.append(data)
                
                # 检查是否达到批处理条件
                if len(batch) >= self.batch_size or \
                   time.time() - last_process_time >= self.batch_timeout:
                    self._handle_batch(batch)
                    batch = []
                    last_process_time = time.time()
                    
            except queue.Empty:
                time.sleep(0.1)
                continue
    
    def _handle_batch(self, batch):
        """处理批次数据"""
        print(f"处理批次数据，共 {len(batch)} 条记录")
        # 实现您的批处理逻辑

# 在 WebSocket 客户端中使用
class BatchedWebSocketClient(StockWebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.batch_processor = BatchDataProcessor()
    
    def on_message(self, message):
        if isinstance(message, bytes):
            packet = DataUtil.process_data(message)
            self.batch_processor.add_data(packet)
        else:
            try:
                data = json.loads(message)
                self.batch_processor.add_data(data)
            except:
                pass
```

### 2. 数据过滤和路由（扩展示例）

```python
class FilteredWebSocketClient(StockWebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.filters = {}
        self.handlers = {}
    
    def add_filter(self, code_pattern, handler):
        """添加过滤器和处理器"""
        self.filters[code_pattern] = handler
    
    def on_message(self, message):
        if isinstance(message, bytes):
            packet = DataUtil.process_data(message)
            self._route_data(packet)
        else:
            try:
                data = json.loads(message)
                self._route_data(data)
            except:
                pass
    
    def _route_data(self, data):
        """根据数据内容路由到不同处理器"""
        if isinstance(data, dict) and 'code' in data:
            code = data['code']
            for pattern, handler in self.filters.items():
                if pattern in code or pattern == '*':  # * 表示所有
                    handler(data)
                    break

# 使用示例
def handle_pingan_bank(data):
    print(f"平安银行数据: {data}")

def handle_all_stocks(data):
    print(f"所有股票数据: {data}")

client = FilteredWebSocketClient(ws_url)
client.add_filter("000001", handle_pingan_bank)
client.add_filter("*", handle_all_stocks)
```

## 性能优化建议

### 1. 连接管理

- **复用连接**：避免频繁创建和销毁 WebSocket 连接
- **合理订阅**：只订阅需要的股票，避免不必要的带宽消耗
- **超时设置**：设置合理的连接超时时间

### 2. 数据处理

- **异步处理**：将数据处理移到单独线程，避免阻塞 WebSocket 接收
- **批量处理**：对高频数据进行批量处理以提高效率
- **内存管理**：及时清理不需要的数据，避免内存泄漏

### 3. 错误恢复

- **重连机制**：实现自动重连功能
- **心跳检测**：定期发送心跳包检测连接状态
- **日志记录**：记录关键事件便于问题排查

## 常见问题

### Q1: 连接失败怎么办？

**排查步骤**：

1. **检查 Token 是否正确**
   ```python
   from tickplus.scripts.Config import Config
   print(f"当前Token: {Config.TOKEN}")
   ```

2. **检查网络连接**
   ```python
   import socket
   try:
       socket.create_connection(("ws.tickplus.org", 80), timeout=5)
       print("网络连接正常")
   except Exception as e:
       print(f"网络连接失败: {e}")
   ```

3. **确认专业版权限**
   - WebSocket 功能需要专业版权限
   - 请登录官网确认您的账户权限

4. **获取官方示例代码**
   - 如果仍然无法连接，建议从 GitHub 获取最新示例代码
   - GitHub 地址：https://github.com/tickplusx/TickPlusSkill
   - 参考 `tickplus/scripts/StockWebSocketClient.py` 的完整实现

```python
try:
    if not client.connect(timeout=30):
        print("连接超时，请检查网络和Token")
except Exception as e:
    print(f"连接异常: {e}")
```

### Q2: 收不到数据？

**排查步骤**：

1. **确认已成功订阅**
   ```python
   # 检查 subscribe() 返回值
   result = client.subscribe(token, auth_codes)
   if result:
       print("订阅成功")
   else:
       print("订阅失败，请检查连接状态")
   ```

2. **检查交易时间**
   - A股交易时间：09:30-11:30, 13:00-15:00
   - 集合竞价时间：09:15-09:25
   - 非交易时间可能无数据推送

3. **验证股票代码格式**
   ```python
   # 正确的格式示例
   auth_codes = ["auction", "000001.SZ", "600000.SH"]
   # 错误格式："000001" (缺少市场后缀)
   ```

4. **启用调试模式**
   ```python
   # 在 connect() 方法中修改
   websocket.enableTrace(True)  # 查看详细握手信息
   ```

5. **添加详细日志**
   ```python
   def on_message(self, message):
       print(f"收到消息类型: {type(message)}")
       print(f"消息长度: {len(message) if message else 0}")
       # ... 其他处理逻辑
   ```

6. **参考官方示例**
   - 运行官方测试脚本：`python tickplus/scripts/StockWebSocketClient.py`
   - GitHub 地址：https://github.com/tickplusx/TickPlusSkill

### Q3: 如何处理大量数据？（扩展示例）

> 以下为性能优化扩展示例，实际使用时请根据需求调整。

```python
# 使用队列和异步处理
import queue
import threading

class HighPerformanceClient(StockWebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.data_queue = queue.Queue(maxsize=10000)
        self.workers = []
        
        # 启动多个工作线程
        for i in range(3):
            worker = threading.Thread(target=self._worker, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def _worker(self, worker_id):
        """工作线程"""
        while True:
            try:
                data = self.data_queue.get(timeout=1)
                self._process_data(data, worker_id)
                self.data_queue.task_done()
            except queue.Empty:
                continue
    
    def on_message(self, message):
        if isinstance(message, bytes):
            packet = DataUtil.process_data(message)
            try:
                self.data_queue.put_nowait(packet)
            except queue.Full:
                print("队列已满，丢弃数据")
```

### Q4: 如何获取最新的示例代码？

如果遇到任何问题，建议从 GitHub 获取最新的官方示例代码：

1. **访问 GitHub 项目**
   - 项目地址：https://github.com/tickplusx/TickPlusSkill

2. **克隆或下载代码**
   ```bash
   git clone https://github.com/tickplusx/TickPlusSkill.git
   cd TickPlusSkill
   ```

3. **查看 WebSocket 示例**
   - 文件路径：`tickplus/scripts/StockWebSocketClient.py`
   - 运行测试：`python tickplus/scripts/StockWebSocketClient.py`

4. **参考文档**
   - SKILL 文档：`tickplus/SKILL.md`
   - API 文档：`tickplus/references/apidoc.md`

## 完整示例

以下是一个完整的 WebSocket 客户端使用示例：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TickPlus WebSocket 完整示例
展示如何连接、订阅、接收和处理实时股票数据
"""

import json
import time
import signal
import sys
from datetime import datetime

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
    
    def on_open(self):
        """连接打开回调"""
        super().on_open()
        self.start_time = time.time()
        print("开始订阅股票数据...")
        
        # 订阅一些示例股票
        token = Config.TOKEN
        auth_codes = ["auction", "000001.SZ", "600000.SH", "000002.SZ"]
        self.subscribe(token, auth_codes)
    
    def on_message(self, message):
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
    
    def on_error(self, error):
        """错误回调"""
        super().on_error(error)
        print(f"WebSocket 错误: {error}")
    
    def on_close(self, close_status_code, close_msg):
        """关闭回调"""
        super().on_close(close_status_code, close_msg)
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
            
            # 运行指定时长
            start_time = time.time()
            while self.running and (time.time() - start_time) < duration:
                time.sleep(1)
            
            print("运行结束，断开连接...")
            self.disconnect()
        else:
            print("无法连接到 WebSocket 服务器")


def main():
    """主函数"""
    # 配置
    token = Config.TOKEN
    ws_url = f"ws://ws.tickplus.org/ws/{token}"
    
    # 创建并运行客户端
    client = CompleteExampleClient(ws_url)
    client.run(duration=30)  # 运行30秒


if __name__ == "__main__":
    main()
```

## 相关资源

- [TickPlus 官方网站](http://www.tickplus.org)
- [GitHub 项目地址](https://github.com/tickplusx/TickPlusSkill) - **获取最新示例代码**
- [API 文档](apidoc.md)
- [SKILL 文档](../SKILL.md)
- [StockWebSocketClient 源码](../scripts/StockWebSocketClient.py)

## 技术支持

如有问题，请访问以下资源：

1. **GitHub 项目**：https://github.com/tickplusx/TickPlusSkill
   - 获取最新示例代码
   - 查看 Issues 和解决方案
   - 提交问题反馈

2. **官方网站**：http://www.tickplus.org
   - 获取技术支持
   - 查看最新文档
   - 账户和权限管理

3. **运行官方测试**
   ```bash
   # 从 GitHub 克隆项目后
   python tickplus/scripts/StockWebSocketClient.py
   ```