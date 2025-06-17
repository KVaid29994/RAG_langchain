from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv

load_dotenv()

response = openai.images.generate(
    model="dall-e-3",
    prompt="A futuristic cityscape at sunset with flying cars",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
print("Generated image URL:", image_url)