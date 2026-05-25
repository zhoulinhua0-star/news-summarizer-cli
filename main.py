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
        "🚀 [bold magenta]Mini AI News Summarizer[/bold magenta]\n[dim]Version 3.0 • Powered by GitHub Actions & ServerChan[/dim]",
        title="[bold green]System Boot[/bold green]",
        border_style="magenta",
        padding=(1, 3)
    ))

    # 2. 获取新闻（使用带地球旋转动画的加载状态）
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

    # 用于聚合微信推送内容的变量
    aggregated_summary = "# 📅 今日 AI 新闻硬核简报\n\n"
    has_valid_content = False

    # 3. 遍历新闻，生成并打印总结
    for i, article in enumerate(articles, 1):
        title = article.get("title") or "No Title Available"
        description = article.get("description") or ""
        url = article.get("url") or "No URL"

        # 使用亮青色打印新闻标题
        console.print(f"\n[bold cyan]📰 [News {i}]: {title}[/bold cyan]")
        console.print(f"[dim]🔗 Link: {url}[/dim]")

        # 处理空内容
        if not description or description.isspace():
            console.print(Panel(
                "[yellow]⚠️ This article lacks sufficient body text for AI to summarize.[/yellow]",
                border_style="yellow"
            ))
            continue

        # 4. 调用 Groq AI
        with console.status("[bold green]AI is reading and digesting...[/bold green]", spinner="dots"):
            summary = summarize_article(title, description)

        # 5. 用 Markdown 格式将 AI 的 Bullet Points 渲染在漂亮的绿色面板里
        console.print(Panel(
            Markdown(summary),
            title="[bold green]🤖 AI Summary[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

        # 6. 将内容拼接到微信推送文本中
        aggregated_summary += f"### 📰 [{i}] {title}\n{summary}\n\n---\n\n"
        has_valid_content = True

    # 打印高亮横幅
    console.print(f"\n[bold reverse green] ✅ All {limit} news stories processed successfully! [/bold reverse green]\n")

    # 7. 触发微信一键推送
    if has_valid_content:
        with console.status("[bold green]Sending today's digest to your WeChat...[/bold green]", spinner="dots"):
            success = push_to_wechat("📅 您有一份新的 AI 新闻早报", aggregated_summary)
            if success:
                console.print("[bold green]✨ [WeChat Push Success] Delivered to your phone![/bold green]\n")
            else:
                console.print("[bold red]❌ [WeChat Push Failed] Please check your ServerChan config.[/bold red]\n")


if __name__ == "__main__":
    main()