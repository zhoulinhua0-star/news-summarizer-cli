import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def push_to_wechat(title: str, markdown_content: str) -> bool:
    """
    使用 PushPlus 将新闻推送到微信
    """
    token = os.getenv("PUSHPLUS_TOKEN")

    if not token:
        print("[错误] 未找到 PUSHPLUS_TOKEN，放弃推送。")
        return False

    url = "http://www.pushplus.plus/send"

    # PushPlus 的请求格式
    data = {
        "token": token,
        "title": title,
        "content": markdown_content,
        "template": "markdown"  # 完美适配你的 AI 生成的 Markdown 格式
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 200:
            return True
        else:
            print(f"[推送失败] PushPlus返回错误: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"[推送异常]: {e}")
        return False