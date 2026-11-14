"""Generate the Markdown API reference from TickPlus apidoc.json."""

import argparse
import json
from pathlib import Path


AUTH_NAMES = {1: "基础版", 2: "高级版", 3: "专业版"}
SDK_METHODS = {
    "/plus/basic/list": "BasicApi.getStockList",
    "/plus/basic/fullquotes": "BasicApi.getFullQuotes",
    "/plus/basic/daykline": "BasicApi.getDayKline",
    "/plus/basic/fullmetric": "BasicApi.getFullMetric",
    "/plus/basic/financecore": "BasicApi.getFinanceCore",
    "/plus/basic/capital": "BasicApi.getCapital",
    "/plus/basic/updatedaykline": "BasicApi.getUpdateDayKline",
    "/plus/pro/timekline": "ProApi.getTimeKline",
    "/plus/pro/gncgf": "ProApi.getGncgf",
    "/plus/pro/minutekline": "ProApi.getMinuteKline",
    "/plus/pro/fullminute": "ProApi.getFullMinute",
    "/plus/pro/fullminutesnapshot": "ProApi.getFullMinuteSnapshot",
    "/plus/expert/transaction": "ExpertApi.getTransaction",
    "/plus/expert/fivelevel": "ExpertApi.getFiveLevel",
    "/plus/expert/fullbid": "ExpertApi.getFullBid",
    "/plus/expert/fluctuation": "ExpertApi.getFluctuation",
}


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(value or "").replace("|", "&#124;").replace("\n", "<br>") for value in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def format_api(api, index):
    auth = "、".join(
        f"{AUTH_NAMES.get(level, f'权限{level}')} ({level})" for level in api.get("apiAuth", [])
    )
    lines = [
        f"### {index}. {api['name']}",
        "",
        api.get("description", ""),
        "",
        f"- **路径**：`{api['url']}`",
        f"- **权限**：{auth}",
    ]
    tags = api.get("tags", [])
    if tags:
        lines.append(f"- **标签**：{'、'.join(tags)}")
    lines.extend(["", "**请求参数**", ""])
    inputs = [
        [p.get("name"), p.get("type"), "是" if p.get("required") else "否", p.get("range"), p.get("description")]
        for p in api.get("inputParas", [])
    ]
    lines.extend(markdown_table(["参数名", "类型", "必填", "取值范围", "说明"], inputs).splitlines())
    lines.extend(["", "**返回字段**", ""])
    outputs = [[p.get("name"), p.get("type"), p.get("description")] for p in api.get("outputParas", [])]
    lines.extend(markdown_table(["字段名", "类型", "说明"], outputs).splitlines())

    demo = api.get("demo")
    if demo:
        lines.extend(["", "**请求示例**", "", "```text", demo, "```"])
    data = api.get("data")
    if data:
        try:
            sample = json.dumps(json.loads(data), ensure_ascii=False, indent=2)
        except (TypeError, json.JSONDecodeError):
            sample = str(data)
        lines.extend(["", "**响应示例**", "", "```json", sample, "```"])
    return "\n".join(lines)


def render(document):
    sections = [
        "# TickPlus API 接口文档",
        "",
        "本文由 TickPlus `apidoc.json` 生成，接口名称、参数、返回字段、示例和权限以该文件为准。",
        "",
        "- **官方网站**：http://www.tickplus.org",
        "- **API 基址**：http://api.tickplus.org",
        "- **请求方式**：GET",
        "",
        "权限代码：1 基础版，2 高级版，3 专业版。",
    ]
    index = 1
    for group in document:
        sections.extend(["", f"## {group['name']}", ""])
        for api in group.get("docApis", []):
            sections.extend([format_api(api, index), ""])
            index += 1
    sections.extend(["", "## Python SDK 方法", "", "| 接口路径 | SDK 方法 |", "| --- | --- |"])
    for group in document:
        for api in group.get("docApis", []):
            method = SDK_METHODS.get(api["url"], "")
            sections.append(f"| `{api['url']}` | `{method}` |")
    return "\n".join(sections).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apidoc_json", type=Path, help="TickPlus apidoc.json path")
    parser.add_argument("output_markdown", type=Path, help="Markdown output path")
    args = parser.parse_args()

    document = json.loads(args.apidoc_json.read_text(encoding="utf-8-sig"))
    args.output_markdown.write_text(render(document), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
