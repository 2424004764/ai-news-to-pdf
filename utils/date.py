from datetime import datetime
import calendar


def get_year():
    return datetime.now().year


def convert_iso_to_datetime_str(iso_date_str):
    """
    将 ISO 8601 格式的时间字符串转换为 '年-月-日 时:分:秒' 格式。

    Args:
        iso_date_str (str): 如 "2022-05-14T00:16:56+08:00"

    Returns:
        str: 如 "2022-05-14 00:16:56"
    """
    if iso_date_str is None:
        return None
    try:
        # 1. 解析字符串为 datetime 对象
        # fromisoformat 是 Python 3.7 专为处理 ISO 格式新增的高效方法
        dt_obj = datetime.fromisoformat(iso_date_str)

        # 2. 格式化输出
        # %Y: 年, %m: 月, %d: 日, %H: 24小时制, %M: 分, %S: 秒
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError as e:
        print(f"日期格式解析错误: {e}")
        return None


def get_days_in_month(year_month):
    """
    输入格式: '2026-01'
    输出格式: ['01', '02', ..., '31']
    """
    # 1. 拆分字符串获取年份和月份
    year, month = map(int, year_month.split('-'))

    # 2. 获取该月天数
    _, num_days = calendar.monthrange(year, month)

    # 3. 生成数组，并使用 f-string 格式化为两位数字（不足两位补0）
    return [f"{d:02d}" for d in range(1, num_days + 1)]
