from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class LLMGenerator:
    def __init__(self, api_key=None):
        """Initialize LLM generator."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt, temperature=0.7, max_tokens=1000):
        """Generate text using LLM."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content
