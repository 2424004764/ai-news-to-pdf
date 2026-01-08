from utils.date import get_year
import datetime


def get_current_year() -> str:
    """
    这是一个用于获取当前日历年份的工具。当用户未提供 'year' 参数时，必须先调用此工具来获取当前年份，
    以便为 'query_value' 工具提供完整的参数。
    """
    # 实际返回当前年份，例如 "2025"
    return get_year()


def get_current_month() -> int:
    """
    获取当前月份

    Returns:
        当前月份，范围 1-12
    """
    return datetime.datetime.now().month


def get_current_date() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_current_xn() -> str:
    """
    获取当前学年，格式为 'YYYY-YYYY+1'
    如当前年为2024年，返回 '2024-2025'
    """
    current_year = datetime.datetime.now().year
    return f"{current_year}-{current_year + 1}"


def get_current_xq() -> int:
    """
    获取当前学期
    如果当前时间在6月30日及以前，返回1（第一学期）
    如果当前时间在7月1日及以后，返回2（第二学期）
    """
    today = datetime.datetime.now()

    # 创建6月30日的日期
    june_30 = datetime.datetime(today.year, 6, 30)

    # 判断当前日期是否在6月30日之前（含当天）
    if today <= june_30:
        return 1  # 第一学期
    else:
        return 2  # 第二学期
