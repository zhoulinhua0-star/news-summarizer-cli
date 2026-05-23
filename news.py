import os
import requests

def get_top_news(limit=3):
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        raise ValueError("Lack NEWS_API_KEY，please make sure it's properly set in .env file")

    # 获取美国当天的头条新闻
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()
    articles = data.get("articles")

    return articles[:limit]