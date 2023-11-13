from django.conf import settings
import openai
from openai import OpenAI
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_llm_response(prompt):
    if not settings.OPENAI_API_KEY:
        logger.error("OpenAI API key is not set.")
        return "Error: OpenAI API key is not set."

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error("An error occurred in OpenAI API interaction: %s", str(e))
        return "Error: Unable to get response."
