import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from fastapi.responses import FileResponse
import uvicorn

load_dotenv()
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    logger.error("OPENROUTER_API_KEY not found.")
    raise ValueError("OPENROUTER_API_KEY not found.")

class GenerateRequest(BaseModel):
    prompt: str

def generate_blog(prompt: str, max_words: int = 1000) -> str:
    try:
        desired_tokens = int(max_words / 0.75)

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [{"role": "user", "content": f"Write a blog about {prompt}"}],
            "max_tokens": desired_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "n": 1,
            "stop": None
        }
        logger.info("Sending request to OpenRouter API...")
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            logger.error(f"API error {response.status_code}: {response.text}")
            return ""

        generated_text = response.json()["choices"][0]["message"]["content"].strip()
        words = generated_text.split()
        if len(words) > max_words:
            truncated = ' '.join(words[:max_words])
            last_period = truncated.rfind('.')
            if last_period != -1:
                truncated = truncated[:last_period + 1]
            generated_text = truncated

        logger.info(f"Generated blog length: {len(generated_text.split())} words")
        return generated_text

    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return ""

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.post("/generate")
async def generate(request: GenerateRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")

    try:
        generated_blog = generate_blog(prompt, 1000)
        if not generated_blog:
            raise HTTPException(status_code=500, detail="Blog generation failed")
        return {"blog": generated_blog}
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")