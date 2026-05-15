
import gzip
import json
import zipfile
from io import BytesIO
import requests


staticmethod


def detect_compression_format(data: bytes) -> str:
    if len(data) >= 4 and (data[0] & 0xFF) == 0x50 and (data[1] & 0xFF) == 0x4B and (
            ((data[2] & 0xFF) == 0x03 and (data[3] & 0xFF) == 0x04) or
            ((data[2] & 0xFF) == 0x05 and (data[3] & 0xFF) == 0x06) or
            ((data[2] & 0xFF) == 0x07 and (data[3] & 0xFF) == 0x08)
    ):
        return "zip"
    elif len(data) >= 2 and (data[0] & 0xFF) == 0x1F and (data[1] & 0xFF) == 0x8B:
        return "gzip"
    return "unknown"

staticmethod
def process_zip_data(data: bytes) :
    try:
        with zipfile.ZipFile(BytesIO(data)) as zip_file:
            for file_info in zip_file.filelist:
                if file_info.filename.endswith('.json'):
                    content = zip_file.read(file_info).decode('utf-8')
                    packet = json.loads(content)
                    return packet
    except Exception as e:
        print(f"解析ZIP数据失败: {e}")

staticmethod
def process_gzip_data(data: bytes):
    try:
        with gzip.GzipFile(fileobj=BytesIO(data)) as gzip_file:
            content = gzip_file.read().decode('utf-8')
            packet = json.loads(content)
            return packet
    except Exception as e:
        print(f"解析GZIP数据失败: {e}")


staticmethod


def process_data(data: bytes):
    compression_format = detect_compression_format(data)
    if compression_format == "gzip":
        return process_gzip_data(data)
    elif compression_format == "zip":
        return process_zip_data(data)
    else:
        return data.decode('utf-8')


staticmethod
def request(url: str, method: str = "get", params=None):
    if method == 'post':
        response = requests.post(url, params=params)
        return response.content.decode('utf-8')
    else:
        response = requests.get(url, params=params)
        return response.content.decode('utf-8')


def printLog(apiName: str, params: dict, data: json):
    if isinstance(data, list):
        print(f"{apiName}，返回 {len(data)} 条记录，参数{params}，数据样例：{data[0] if len(data) > 0 else {} }")
    else:
        print(f"{apiName}，返回异常信息，参数{params}，异常详情：{data}")
    return data
