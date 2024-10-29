from typing import List, Dict, Optional
import requests
from confluence_client import ConfluenceClient

MODEL = "llama2"
BASE_URL = "http://localhost:11434"


class OllamaClient:
    """Класс для работы с Ollama API с использованием данных из Confluence"""

    def __init__(self, base_url: str = BASE_URL, model: str = MODEL):
        """
        Инициализация клиента Ollama

        Args:
            base_url (str): Базовый URL сервера Ollama
            model (str): Название модели для использования
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.confluence_client = ConfluenceClient()

    def _make_ollama_request(self, prompt: str) -> Optional[str]:
        """
        Отправка запроса к Ollama API

        Args:
            prompt (str): Промпт для модели

        Returns:
            Optional[str]: Ответ от модели или None в случае ошибки
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get('response')
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Ollama: {e}")
            return None

    def _format_context(self, confluence_results: List[Dict[str, str]]) -> str:
        """
        Форматирование результатов из Confluence в контекст для промпта

        Args:
            confluence_results: Список результатов из Confluence

        Returns:
            str: Отформатированный контекст
        """
        context = "Контекст из Confluence:\n\n"
        for idx, result in enumerate(confluence_results, 1):
            context += f"Документ {idx}:\n"
            context += f"Заголовок: {result['title']}\n"
            context += f"Содержание: {result['content']}\n\n"
        return context

    def generate_with_rag(self, confluence_query: str, llm_query: str, max_confluence_results: int = 3) -> Optional[str]:
        """
        Генерация ответа с использованием RAG-подхода

        Args:
            confluence_query (str): Пользовательский запрос в confluence
            llm_query (str): Пользовательский запрос в llm
            max_confluence_results (int): Максимальное количество результатов из Confluence

        Returns:
            Optional[str]: Ответ от модели или None в случае ошибки
        """
        # Поиск релевантных документов в Confluence
        confluence_results = self.confluence_client.search(confluence_query, max_confluence_results)

        if not confluence_results:
            print("Не найдено релевантных документов в Confluence")
            # Делаем запрос к модели без дополнительного контекста
            return self._make_ollama_request(llm_query)

        # Форматируем контекст из результатов Confluence
        context = self._format_context(confluence_results)

        # Формируем обогащенный промпт
        enriched_prompt = (
            f"На основе следующего контекста ответь на вопрос.\n\n"
            f"{context}\n"
            f"Вопрос: {llm_query}\n"
            f"Ответ:"
        )
        print(enriched_prompt)
        # Отправляем обогащенный промпт к Ollama
        return self._make_ollama_request(enriched_prompt)

    def generate_simple(self, prompt: str) -> Optional[str]:
        """
        Простая генерация без использования RAG

        Args:
            prompt (str): Промпт для модели

        Returns:
            Optional[str]: Ответ от модели или None в случае ошибки
        """
        return self._make_ollama_request(prompt)