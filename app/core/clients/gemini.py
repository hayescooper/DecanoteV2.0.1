"""Client gọi Gemini. Khóa lấy từ biến môi trường, không hard-code."""
import os


def audit(prompt: str) -> str:
    from google import genai  # import trễ để test không cần cài/khóa

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Thiếu GEMINI_API_KEY trong file .env")

    model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text or ""
