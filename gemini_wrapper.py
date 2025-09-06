import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class GeminiWrapper:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Use newer model for better reasoning
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash',
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def generate_response(self, prompt: str) -> str:
        """Synchronous response generation"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def generate_response_async(self, prompt: str) -> str:
        """Asynchronous response generation"""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
