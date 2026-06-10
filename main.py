import os
import re
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from news import get_top_news
from summarize import summarize_article
from push import push_to_wechat

# 初始化 rich 控制台
console = Console()


def build_hardcore_html(news_list, digest_title="AI Hardcore Daily") -> str:
    """
    根据硬核 UI 模板生成最终的 HTML 字符串 (English Version)
    智能容错解析，确保 AI 生成的内容一字不差地被填入模板
    """
    weeks = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    bj_tz = timezone(timedelta(hours=8))
    today = datetime.now(bj_tz)
    date_str = f"{today.strftime('%b %d, %Y')} {weeks[today.weekday()]} · {len(news_list)} Stories"

    # 为所有 6 个新分类 + General 专属定制的高颜值调色盘
    category_styles = {
        "tech": "background:#F5F3FF;color:#6D28D9;border:1px solid #DDD6FE;",  # 紫色
        "business": "background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;",  # 黄色/琥珀
        "sports": "background:#ECFDF5;color:#047857;border:1px solid #A7F3D0;",  # 绿色
        "politics": "background:#FEF2F2;color:#B91C1C;border:1px solid #FCA5A5;",  # 红色
        "world": "background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;",  # 蓝色
        "entertainment": "background:#FDF2F8;color:#BE185D;border:1px solid #FBCFE8;",  # 粉色
        "general": "background:#FAFAFA;color:#52525B;border:1px solid #E4E4E7;",  # 灰色
        "default": "background:#FAFAFA;color:#52525B;border:1px solid #E4E4E7;"
    }

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{digest_title}</title>
  <style>
    html, body {{ margin: 0; padding: 0; background: #ECECEC; }}
    body {{ max-width: 430px; margin: 0 auto; min-height: 100vh; box-shadow: 0 0 24px rgba(0,0,0,0.08); }}
  </style>
</head>
<body>
  <div style="font-family:-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;background:#FFFFFF;padding:12px 10px 16px 10px;color:#171717;word-break:normal;overflow-wrap:break-word;-webkit-text-size-adjust:100%;">
    <div style="margin-bottom:18px;padding-bottom:14px;border-bottom:2px solid #07C160;">
      <div style="font-size:20px;font-weight:700;line-height:1.3;color:#171717;margin:0 0 6px 0;">{digest_title}</div>
      <div style="font-size:13px;line-height:1.5;color:#737373;margin:0;">{date_str}</div>
    </div>
"""

    for i, item in enumerate(news_list, start=1):
        index_str = f"{i:02d}"
        category = item.get('category', 'General')
        badge_style = category_styles.get(category.lower(), category_styles['default'])

        title = item.get('title', 'No Title')
        source = item.get('source', 'Unknown Source')
        time_str = item.get('time', 'Today')
        url = item.get('url', '#')

        summary_raw = item.get('summary', '').strip()
        points = []

        li_matches = re.findall(r'<li>(.*?)</li>', summary_raw, re.DOTALL)
        if li_matches:
            points = [p.strip() for p in li_matches if p.strip()]

        if not points:
            clean_text = re.sub(r'</?(ul|ol|p|div|span)[^>]*>', '', summary_raw)
            lines = clean_text.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    line = re.sub(r'^([•\-*\d+\.]+)\s*', '', line).strip()
                    if line:
                        points.append(line)

        if not points and summary_raw:
            points = [re.sub(r'<[^>]+>', '', summary_raw).strip()]

        table_rows_html = ""
        for pt in points:
            if pt:
                table_rows_html += f"""
          <tr><td style="padding:0 0 10px 0;vertical-align:top;width:16px;color:#07C160;font-size:15px;line-height:1.65;">•</td><td style="padding:0 0 10px 6px;color:#404040;font-size:15px;line-height:1.65;word-break:normal;overflow-wrap:break-word;">{pt}</td></tr>"""

        html_content += f"""
    <div style="margin-bottom:16px;background:#FAFAFA;border:1px solid #E5E5E5;border-radius:10px;overflow:hidden;word-break:normal;overflow-wrap:break-word;">
      <div style="padding:14px 14px 0 14px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;">
          <tr>
            <td style="width:36px;vertical-align:top;padding:0 10px 0 0;">
              <div style="display:inline-block;min-width:32px;text-align:center;background:#07C160;color:#FFFFFF;font-size:13px;font-weight:700;line-height:32px;border-radius:8px;">{index_str}</div>
            </td>
            <td style="vertical-align:top;padding:0;">
              <span style="display:inline-block;margin:0 0 8px 0;padding:2px 8px;{badge_style}font-size:11px;font-weight:600;line-height:1.4;border-radius:999px;letter-spacing:0.02em;">{category}</span>
              <div style="color:#171717;font-size:16px;font-weight:600;line-height:1.45;margin:0 0 6px 0;word-break:normal;overflow-wrap:break-word;">{title}</div>
              <div style="color:#737373;font-size:12px;line-height:1.4;margin:0 0 12px 0;">{source} · {time_str}</div>
            </td>
          </tr>
        </table>
      </div>
      <div style="padding:0 14px 12px 14px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;">
          {table_rows_html}
        </table>
      </div>
      <div style="padding:8px 14px 12px 14px;border-top:1px solid #E5E5E5;">
        <a href="{url}" style="color:#576B95;font-size:11px;line-height:1.3;text-decoration:none;word-break:break-all;">Read Full Article →</a>
      </div>
    </div>
"""

    html_content += """
    <div style="margin-top:4px;padding-top:12px;border-top:1px solid #E5E5E5;text-align:center;color:#737373;font-size:11px;line-height:1.5;">
      Summary generated by Groq AI · Click link to read full article
    </div>
  </div>
</body>
</html>"""

    return html_content


def main():
    load_dotenv()

    console.print(Panel.fit(
        "🚀 [bold magenta]Mini AI News Summarizer[/bold magenta]\n[dim]Version 5.2 • 6-Category Extended UI[/dim]",
        title="[bold green]System Boot[/bold green]",
        border_style="magenta",
        padding=(1, 3)
    ))

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

    processed_news = []

    for i, article in enumerate(articles, 1):
        title = article.get("title") or "No Title Available"
        description = article.get("description") or ""
        url = article.get("url") or "No URL"

        source_name = "Unknown Source"
        if isinstance(article.get("source"), dict):
            source_name = article.get("source").get("name", "Unknown Source")

        published_at = "Today"
        if article.get("publishedAt"):
            published_at = str(article.get("publishedAt"))[:10]

        console.print(f"\n[bold cyan]📰 [News {i}]: {title}[/bold cyan]")
        console.print(f"[dim]🔗 Link: {url}[/dim]")

        if not description or description.isspace():
            console.print(Panel("[yellow]⚠️ This article lacks sufficient body text.[/yellow]", border_style="yellow"))
            continue

        with console.status("[bold green]AI is reading and digesting...[/bold green]", spinner="dots"):
            raw_ai_response = summarize_article(title, description)

        # ==========================================
        # ✂️ 智能拆解逻辑（已更新为 6 个分类 + General 兜底）
        # ==========================================
        raw_lines = [line.strip() for line in raw_ai_response.strip().split('\n') if line.strip()]

        category = "General"  # 1. 默认分类改为 General
        actual_summary_lines = []

        if raw_lines:
            first_line_lower = raw_lines[0].lower()
            has_category = False

            # 2. 检查大模型返回的第一行是否属于这 6 个新分类
            valid_categories = ["Tech", "Business", "Sports", "Politics", "World", "Entertainment"]
            for valid_cat in valid_categories:
                if valid_cat.lower() in first_line_lower:
                    category = valid_cat  # 保留完美的大小写
                    has_category = True
                    break

            if has_category:
                actual_summary_lines = raw_lines[1:]
            else:
                # 容错：如果 AI 没有返回分类，所有内容均视作正文，标签使用默认的 General
                actual_summary_lines = raw_lines

        actual_summary = '\n'.join(actual_summary_lines)
        # ==========================================

        console.print(Panel(
            Markdown(actual_summary),
            title=f"[bold green]🤖 AI Summary ({category})[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

        processed_news.append({
            "title": title,
            "url": url,
            "summary": actual_summary,
            "source": source_name,
            "time": published_at,
            "category": category
        })

    console.print(f"\n[bold reverse green] ✅ All {limit} news stories processed successfully! [/bold reverse green]\n")

    if processed_news:
        with console.status("[bold green]Generating Hardcore UI and sending to WeChat...[/bold green]", spinner="dots"):
            final_html_string = build_hardcore_html(processed_news, "AI Hardcore Daily")
            success = push_to_wechat("每日新闻", final_html_string)

            if success:
                console.print("[bold green]✨ [WeChat Push Success] Delivered to your phone![/bold green]\n")
            else:
                console.print("[bold red]❌ [WeChat Push Failed] Please check your PushPlus config.[/bold red]\n")


if __name__ == "__main__":
    main()