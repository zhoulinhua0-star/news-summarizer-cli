import os
from openai import OpenAI


def summarize_article(title: str, description: str) -> str:
    """
    Generate news summary using Groq API.
    Returns a concise string with 3 bullet points.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GROQ_API_KEY in .env file.")

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )

    prompt = f"""
    Please read the following news article and complete two tasks:

    1. [Line 1]: Strictly choose the most appropriate category from the following 6 words (Tech, Business, Sports, Politics, World, Entertainment). Output ONLY this single word on the first line. Do not include any other characters or labels. If it doesn't fit any, output 'General'.
    2. [Line 2 and onwards]: Summarize the article into exactly 3 concise, objective, and easy-to-read bullet points in English. You MUST wrap each bullet point in <li> tags.

    News Article:
    Title: {str(title)}
    Content: {str(description)}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional news editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=256
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Catch API-level errors
        return f"⚠️ Fails to generate summarization: {e}"