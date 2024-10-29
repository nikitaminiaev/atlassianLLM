# Создание клиента
from ollamaClient import OllamaClient


def main():
    # Ввод запросов от пользователя
    confluence_query = input("Введите запрос для Confluence: ")
    llm_query = input("Введите запрос для LLM: ")

    # Ввод max_confluence_results (опционально)
    max_confluence_results_input = input("Введите максимальное количество результатов из Confluence (по умолчанию 5): ")
    max_confluence_results = int(max_confluence_results_input) if max_confluence_results_input else 5

    # Создание клиента
    ollama_client = OllamaClient(model="nemotron-mini")

    # Генерация ответа с использованием RAG
    response = ollama_client.generate_with_rag(confluence_query, llm_query, max_confluence_results)
    print("Ответ:", response)


if __name__ == "__main__":
    main()
# # Простая генерация без RAG
# simple_response = ollama_client.generate_simple(
#     "Что такое CI/CD?"
# )
# print(simple_response)
