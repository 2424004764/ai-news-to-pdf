import requests
import socket


class BaiduSearch:
    base_url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    api_key = ""

    def search(self, query):
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
