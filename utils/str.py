import json
from typing import Dict, Any


def str_to_json(json_str: str) -> Dict[str, Any]:
    """
    同步解析 Agent 返回的 JSON 字符串，并处理解析错误。

    Args:
        json_str: Agent 返回的原始字符串。

    Returns:
        解析后的 Python 字典，如果解析失败则返回一个错误字典。
    """
    try:
        # 尝试将字符串解析为字典
        json_object = json.loads(json_str)
        return json_object

    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}. 原始字符串: {json_str[:100]}...")
        return {}
