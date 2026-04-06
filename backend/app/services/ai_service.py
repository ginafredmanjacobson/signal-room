import logging
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_brief(cluster_items_texts: list, topic: str) -> dict:
    """Generate a summary and bullet points for a cluster using OpenAI."""
    if settings.AI_MODE == "mock":
        # Return mock data
        combined = " ".join(cluster_items_texts)[:500]
        return {
            "summary": f"Summary of '{topic}': " + combined[:200] + "...",
            "bullets": [
                "Mock bullet point 1 based on trends.",
                "Mock bullet point 2 highlighting key insight.",
                "Mock bullet point 3 with potential campaign angle."
            ]
        }
    
    try:
        prompt = f"""You are a cultural insights analyst. Below are posts related to the topic "{topic}". 
Please provide:
1. A concise summary (2-3 sentences) of the main themes.
2. Three bullet points with actionable insights for a marketing campaign.

Posts:
{chr(10).join(cluster_items_texts[:5])}  # limit to first 5 to avoid token overflow
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        content = response.choices[0].message.content
        # Simple parsing: assume first paragraph is summary, rest bullets
        parts = content.split("\n")
        summary = parts[0] if parts else ""
        bullets = [line.strip("-• ") for line in parts[1:] if line.strip()]
        return {
            "summary": summary,
            "bullets": bullets[:3]
        }
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return {
            "summary": "Error generating summary.",
            "bullets": ["Try again later."]
        }

def summarize_text(text: str):
    if settings.AI_MODE == "mock":
        clean = text.strip().replace("\n", " ")
        return {
            "summary": clean[:220] + ("..." if len(clean) > 220 else ""),
            "bullets": [b.strip() for b in clean.split(".")[:3] if b.strip()]
        }
    # Add real implementation if needed later