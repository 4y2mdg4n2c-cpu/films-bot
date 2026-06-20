import requests
import certifi
import time
def get_films(title, api_key):
    url = f'https://www.omdbapi.com/?s={title}&apikey={api_key}'
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                timeout=10,
                verify=certifi.where()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Попытка {attempt + 1}: таймаут")
            time.sleep(1)
        except requests.exceptions.ConnectionError as e:
            print(f"Попытка {attempt + 1}: ошибка соединения {e}")
            time.sleep(1)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP ошибка: {e}")
            return None
    return None
def get_film_by_id(imdb_id, api_key):
    url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
