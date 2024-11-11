import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


if not OPENROUTER_API_KEY:
    logger.error("OPENROUTER_API_KEY not found. Please set it in the .env file.")
    raise ValueError("OPENROUTER_API_KEY not found. Please set it in the .env file.")

def generate_blog(prompt, max_words=1000):
    """
    Generates a blog post using OpenRouter's LLM API.

    Args:
        prompt (str): The input prompt to generate the blog.
        max_words (int): Desired number of words in the blog.

    Returns:
        str: Generated blog post or an empty string if failed.
    """
    try:
        desired_tokens = int(max_words / 0.75) 

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free", 
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
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
            logger.error(f"OpenRouter API returned status code {response.status_code}: {response.text}")
            return ""
        response_data = response.json()
        generated_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        words = generated_text.split()
        if len(words) > max_words:
            truncated = ' '.join(words[:max_words])
            last_period = truncated.rfind('.')
            if last_period != -1:
                truncated = truncated[:last_period+1]
            generated_text = truncated

        logger.info(f"Generated blog length in words: {len(generated_text.split())}")

        return generated_text

    except Exception as e:
        logger.error(f"Exception in generate_blog: {e}")
        return ""

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    if not prompt:
        logger.warning("No prompt provided in the request.")
        return jsonify({'error': 'No prompt provided.'}), 400

    try:
        logger.info(f"Received prompt: {prompt[:50]}...") 
        generated_blog = generate_blog(prompt, max_words=1000)

        if not generated_blog:
            logger.error("Generated blog is empty.")
            return jsonify({'error': 'Failed to generate blog.'}), 500

        logger.info("Blog generated successfully.")
        return jsonify({'blog': generated_blog})

    except Exception as e:
        logger.error(f"Error in /generate route: {e}")
        return jsonify({'error': 'Failed to generate blog.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
