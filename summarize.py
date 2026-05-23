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

    prompt = f"Summarize this news article in exactly 3 bullet points. Keep it concise, objective, and easy to read.\n\nTitle: {str(title)}\nContent: {str(description)}"

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