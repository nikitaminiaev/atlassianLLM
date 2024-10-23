# Создание клиента
from ollamaClient import OllamaClient

ollama_client = OllamaClient(model="llama2")

# Генерация с использованием RAG
response = ollama_client.generate_with_rag(
    "Как настроить интеграцию с Jira?",
    max_confluence_results=3
)
print(response)

# Простая генерация без RAG
simple_response = ollama_client.generate_simple(
    "Что такое CI/CD?"
)
print(simple_response)