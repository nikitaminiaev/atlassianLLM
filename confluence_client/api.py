import base64
import requests


class ConfluenceAPI:
    """Класс для работы с API Confluence"""

    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Инициализация клиента API

        Args:
            base_url (str): Базовый URL Confluence
            email (str): Email для аутентификации
            api_token (str): API токен для аутентификации
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Accept': 'application/json',
            'Authorization': self._create_auth_header(email, api_token)
        }

    def _create_auth_header(self, email: str, api_token: str) -> str:
        """Создание заголовка авторизации"""
        auth_str = f"{email}:{api_token}"
        auth_bytes = auth_str.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        return f"Basic {base64_auth}"

    def search_content(self, query: str, limit: int = 3) -> dict:
        """
        Поиск контента в Confluence

        Args:
            query (str): Поисковый запрос
            limit (int): Максимальное количество результатов

        Returns:
            dict: Ответ от API с результатами поиска
        """
        url = f"{self.base_url}/rest/api/content/search"
        params = {
            'cql': f'title ~ \'{query}\'',
            'expand': 'body.view',
            'limit': limit
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()