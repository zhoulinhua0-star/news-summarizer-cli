import os
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from news import get_top_news
from summarize import summarize_article

# 初始化 rich 控制台
console = Console()


def main():
    # 1. 加载环境变量
    load_dotenv()

    # 打印欢迎面板
    console.print(Panel.fit(
        "🚀 [bold magenta]Mini AI News Summarizer[/bold magenta]\n[dim]Version 2.0 • Powered by Groq & Llama 3.3[/dim]",
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

    # 打印高亮横幅
    console.print(f"\n[bold reverse green] ✅ All {limit} news stories processed successfully! [/bold reverse green]\n")


if __name__ == "__main__":
    main()