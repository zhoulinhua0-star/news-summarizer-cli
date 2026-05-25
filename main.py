import os
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from news import get_top_news
from summarize import summarize_article
from push import push_to_wechat

# 初始化 rich 控制台
console = Console()


def main():
    # 1. 加载环境变量
    load_dotenv()

    # 打印欢迎面板
    console.print(Panel.fit(
        "🚀 [bold magenta]Mini AI News Summarizer[/bold magenta]\n[dim]Version 4.0 • Premium HTML Card Edition[/dim]",
        title="[bold green]System Boot[/bold green]",
        border_style="magenta",
        padding=(1, 3)
    ))

    # 2. 获取新闻
    limit = 3
    with console.status("[bold blue]Connecting to NewsAPI and fetching headlines...[/bold blue]", spinner="earth"):
        try:
            articles = get_top_news(limit=limit)
        except Exception as e:
            console.print(f"\n[bold red]❌ A critical error occurred while fetching news:[/bold red] {e}")
            return

    if not articles:
        console.print("\n[yellow]📭 No news articles found at the moment.[/yellow]")
        return

    # 3. 初始化微信端 HTML 容器样式（强制规定：整词换行，不许切断英文）
    aggregated_summary = """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; padding: 5px; word-break: normal;">
        <h2 style="color: #191919; margin-bottom: 20px; border-bottom: 2px solid #07c160; padding-bottom: 8px; font-size: 18px;">📅 今日 AI 硬核早报</h2>
    """
    has_valid_content = False

    # 4. 遍历新闻，生成并打印总结
    for i, article in enumerate(articles, 1):
        title = article.get("title") or "No Title Available"
        description = article.get("description") or ""
        url = article.get("url") or "No URL"

        # 本地电脑终端打印（保持炫酷）
        console.print(f"\n[bold cyan]📰 [News {i}]: {title}[/bold cyan]")
        console.print(f"[dim]🔗 Link: {url}[/dim]")

        # 处理空内容
        if not description or description.isspace():
            console.print(Panel(
                "[yellow]⚠️ This article lacks sufficient body text for AI to summarize.[/yellow]",
                border_style="yellow"
            ))
            continue

        # 调用 Groq AI
        with console.status("[bold green]AI is reading and digesting...[/bold green]", spinner="dots"):
            summary = summarize_article(title, description)

        # 本地电脑终端漂亮的绿色面板渲染
        console.print(Panel(
            Markdown(summary),
            title="[bold green]🤖 AI Summary[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

        # 5. 【核心清洗】将 AI 返回的 Markdown 列表符号清洗并转化为完美的 HTML 列表
        lines = [line.strip() for line in summary.split("\n") if line.strip()]
        html_bullets = ""
        for line in lines:
            # 去除 AI 输出可能带有的各种圆点或中划线符号，并清除 Markdown 的加粗符号 **
            clean_line = line.lstrip("•-* ").strip().replace("**", "")
            if clean_line:
                # 每一条总结都强制注入 word-break: normal 确保英文完美换行
                html_bullets += f"<li style='margin-bottom: 8px; text-align: justify; word-break: normal; word-wrap: break-word;'>{clean_line}</li>"

        # 6. 【精装排版】构建极具高级感的 HTML 卡片（带灰色淡雅背景、左侧微信绿高亮条）
        news_card = f"""
        <div style="margin-bottom: 20px; background-color: #f8f9fa; padding: 14px; border-radius: 8px; border-left: 4px solid #07c160; word-break: normal; word-wrap: break-word; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h3 style="margin: 0 0 12px 0; color: #111111; font-size: 15px; line-height: 1.4; word-break: normal; word-wrap: break-word;">📰 {i}. {title}</h3>
            <ul style="padding-left: 18px; margin: 0 0 12px 0; color: #333333; font-size: 14px; line-height: 1.5; word-break: normal; word-wrap: break-word;">
                {html_bullets}
            </ul>
            <div style="margin-top: 10px; border-top: 1px dashed #e0e0e0; padding-top: 8px;">
                <a href="{url}" style="color: #576b95; font-size: 12.5px; text-decoration: none; word-break: break-all;">🔗 点击此处阅读原文</a>
            </div>
        </div>
        """
        aggregated_summary += news_card
        has_valid_content = True

    # 闭合 HTML 标签
    aggregated_summary += "</div>"

    console.print(f"\n[bold reverse green] ✅ All {limit} news stories processed successfully! [/bold reverse green]\n")

    # 7. 触发微信一键推送
    if has_valid_content:
        with console.status("[bold green]Sending today's digest to your WeChat...[/bold green]", spinner="dots"):
            success = push_to_wechat("📅 您有一份新的 AI 新闻早报", aggregated_summary)
            if success:
                console.print("[bold green]✨ [WeChat Push Success] Delivered to your phone![/bold green]\n")
            else:
                console.print("[bold red]❌ [WeChat Push Failed] Please check your PushPlus config.[/bold red]\n")


if __name__ == "__main__":
    main()