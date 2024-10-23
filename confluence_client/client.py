import os
from typing import List, Dict
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import html2text

from .api import ConfluenceAPI


class ConfluenceClient:
    """Класс для работы с Confluence"""

    def __init__(self):
        """Инициализация клиента с загрузкой конфигурации"""
        config = self._load_config()
        self.api = ConfluenceAPI(
            base_url=config['base_url'],
            email=config['email'],
            api_token=config['api_token']
        )

    @staticmethod
    def _load_config() -> Dict[str, str]:
        """Загрузка конфигурации из .env файла"""
        load_dotenv()

        config = {
            'email': os.getenv('CONFLUENCE_EMAIL'),
            'api_token': os.getenv('CONFLUENCE_API_TOKEN'),
            'base_url': os.getenv('CONFLUENCE_URL', 'https://jivosite.atlassian.net/wiki')
        }

        if not all([config['email'], config['api_token']]):
            raise ValueError("Необходимо указать CONFLUENCE_EMAIL и CONFLUENCE_API_TOKEN в .env файле")

        return config

    @staticmethod
    def _clean_html_content(html_content: str) -> str:
        """Очистка HTML-контента и преобразование в читаемый текст"""
        soup = BeautifulSoup(html_content, 'html.parser')

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        clean_text = h.handle(str(soup))

        return '\n'.join(line.strip() for line in clean_text.splitlines() if line.strip())

    def search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Поиск в Confluence с форматированием результатов

        Args:
            query (str): Поисковый запрос
            max_results (int): Максимальное количество результатов

        Returns:
            List[Dict[str, str]]: Список отформатированных результатов
        """
        try:
            data = self.api.search_content(query, max_results)
            results = []

            for item in data.get('results', []):
                content = item.get('body', {}).get('view', {}).get('value', '')
                if content:
                    clean_content = self._clean_html_content(content)
                    results.append({
                        'title': item.get('title', 'Без заголовка'),
                        'content': clean_content[:1000] + '...' if len(clean_content) > 1000 else clean_content,
                        'url': item.get('_links', {}).get('webui', '')
                    })

            return results

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return []