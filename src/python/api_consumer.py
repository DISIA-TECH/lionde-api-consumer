import requests


class APIConsumer:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint: str, params: dict = None):
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}?"
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error GET: {e}")
            return None
