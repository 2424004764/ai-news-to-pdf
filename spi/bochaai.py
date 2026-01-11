import requests
import socket
from utils.date import convert_iso_to_datetime_str, get_days_in_month
import re


class BoChaAiApi:
    def __init__(self):
        self.api_key = ""
        self.base_url = "https://api.bocha.cn/v1"

    socket.setdefaulttimeout(10)

    def search_news(self, query, freshness, day_count):
        params = {
            "query": query,
            "freshness": freshness,
            "summary": True,
            "count": day_count,
            # "exclude": "m.ximalaya.com|zzs.ujs.edu.cn|olyview.com|guilin.gov.cn|english.www.gov.cn",
            "include": "toutiao.com|news.qq.com|cls.cn|163.com"
        }

        session = requests.Session()
        session.trust_env = False  # ✅ 关键：不读系统代理

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        response = session.post(
            f"{self.base_url}/web-search",
            json=params,
            headers=headers,
            timeout=(5, 10),  # (连接超时, 读取超时)
        )

        response.raise_for_status()
        return response.json()

    def clean_content(self, text):
        if not text:
            return ""

        # 1. 剔除所有 PUA 范围的特殊字符 (U+E000 - U+F8FF)
        # 2. 同时剔除换行符、制表符等 (\n, \r, \t)
        # 3. 剔除不可见控制字符 ([\x00-\x1f])
        text = re.sub(r'[\ue000-\uf8ff\n\r\t\x00-\x1f]', '', text)

        # 4. 将多个连续空格合并为一个，并去除首尾空格
        return " ".join(text.split())

    def get_news_by_date(self, query, freshness, day_count):
        data = self.search_news(query, freshness, day_count)

        news_data = []
        if 'code' not in data or data['code'] != 200:
            print(self.__name__ + "请求失败")
            return news_data
        if len(data['data']['webPages']['value']) == 0:
            print(self.__name__ + "没有找到新闻")
            return news_data
        news_data = [
            {
                "title": item['name'],
                "siteName": item['siteName'],
                "date": convert_iso_to_datetime_str(item['datePublished']),
                "content": self.clean_content(item.get('summary'))
            } for item in data['data']['webPages']['value']
            if item.get('datePublished') is not None
               and "点击预约这期" not in item.get('summary')
               and "虎扑社区" not in item.get('name')
        ]
        return news_data

    def get_news(self, ym, incidental, day_count):
        days = get_days_in_month(ym)

        news_data = []
        for idx, day in enumerate(days):
            date = ym + "-" + str(day)
            query = "{} {}".format(date, incidental)
            freshness = "{}..{}".format(ym + "-" + str(day), ym + "-" + str(day))
            data = self.get_news_by_date(query, freshness, day_count)
            news_data.extend(data)
            print(f"第{idx+1}次调用，日期：{date}， freshness：{freshness}，获取的新闻条数：{len(data)}")

        print(f"{ym}调用完成，共获取新闻条数：{len(news_data)}")
        return sorted(news_data, key=lambda x: x['date'])
