from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.ai_config import recipe_by_name_promt, recipe_by_ingridients_promt
import os

load_dotenv()
API_KEY = os.getenv("AI_TOKEN")

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=API_KEY,
)

async def get_recipe_by_name(*, dish_name: str) -> str:
  completion = await client.chat.completions.create(
    model="meta-llama/llama-4-scout:free",
    max_tokens=1000,
    messages=[
      {"role": "system", 
       "content": recipe_by_name_promt,
      },
      {
        "role": "user",
        "content": dish_name
      }
    ]
  )
  return(completion.choices[0].message.content)

async def get_recipe_by_ingridients(*, user_ingridients: str) -> str:
  completion = await client.chat.completions.create(
    model="meta-llama/llama-4-scout:free",
    max_tokens=1000,
    messages=[
      {"role": "system", 
       "content": recipe_by_ingridients_promt,
      },
      {
        "role": "user",
        "content": user_ingridients
      }
    ]
  )
  print(completion)
  return(completion.choices[0].message.content)