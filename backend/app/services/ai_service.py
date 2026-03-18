from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def summarize_text(text: str):
    if settings.AI_MODE == "mock":
        clean = text.strip().replace("\n", " ")
        return {
            "summary": clean[:220] + ("..." if len(clean) > 220 else ""),
            "bullets": [b.strip() for b in clean.split(".")[:3] if b.strip()]
        }



# def summarize_text(text: str):
#     prompt = f"""
#     Summarize the following text in 2–3 sentences.
#     Then extract 3–5 concise bullet points.

#     Text:
#     {text}

#     Return:
#     Summary:
#     - ...
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a precise summarization engine."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     content = response.choices[0].message.content

#     # You can parse this properly later
#     return content