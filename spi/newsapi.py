from urllib.parse import urlencode

import requests
import socket


class NewsApi:
    def __init__(self):
        self.api_key = "49ffdefcd0554a5cb5ec3a5c6f9b7e9d"
        self.base_url = "https://newsapi.org/v2"

    socket.setdefaulttimeout(10)

    def search_news(self, query):
        params = {
            "q": query,
            "apiKey": self.api_key,
        }

        session = requests.Session()
        session.trust_env = False  # ✅ 关键：不读系统代理

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }

        response = session.get(
            f"{self.base_url}/everything",
            params=params,
            headers=headers,
            timeout=(5, 10),  # (连接超时, 读取超时)
            verify=True  # SSL 校验（默认即可）
        )

        response.raise_for_status()
        return response.json()
