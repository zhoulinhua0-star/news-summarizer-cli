# 🚀 Mini AI News Summarizer (Rich Terminal 版)

一个基于 Python 的极简、高颜值命令行 AI 新闻总结工具。它能从 NewsAPI 实时抓取全球最新头条，并通过 Groq API (Llama 3.3 模型) 自动为你提炼出结构清晰、一目了然的 3 点式核心摘要。

本版本采用了 `rich` 库进行控制台美化，摆脱了传统终端丑陋、单调的排版，为你提供带有彩色边框、动态加载动画（Spinner）以及完美 Markdown 渲染的极致命令行阅读体验。

---

## ✨ 功能特性

* **实时抓取**：对接 NewsAPI 官方接口，实时获取最新的美国/全球热门头条新闻。
* **光速总结**：利用 Groq 极其恐怖的推理速度，几秒内完成对多篇新闻的深度阅读与摘要提炼。
* **赛博朋克风 UI**：使用 `rich` 渲染。拥有精美的彩色圆角卡片边框、高亮标题，以及网络请求和 AI 处理时的动态旋转加载条。
* **数据安全**：完美支持 `.env` 环境变量配置，配合 `.gitignore` 彻底杜绝 API 密钥泄露的风险。

---

## 📂 项目文件结构

请确保你的本地文件夹目录保持如下结构：

```text
news-summarizer/
│
├── main.py             # 程序主入口（包含 Rich UI 渲染逻辑）
├── news.py             # 新闻获取模块（负责对接 NewsAPI）
├── summarize.py        # AI 总结模块（负责对接 Groq Llama 3.3）
├── requirements.txt    # 项目第三方依赖依赖包列表
└── .gitignore          # Git 忽略配置文件（保护 .env 安全）
```

---

## MIT License

Copyright (c) 2026 Linhua Zhou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.