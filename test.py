import os
from dotenv import load_dotenv
from films import get_films

load_dotenv()

api_key = os.getenv("API_KEY")
print(api_key)

data = get_films("interstellar", api_key)

print(data)