from .client import ConfluenceClient


def main():
    """Пример использования клиента"""
    try:
        client = ConfluenceClient()
        query = input("Введите поисковый запрос: ")
        results = client.search(query)

        if not results:
            print("Результаты не найдены")
            return

        print("\nНайденные результаты:\n")
        for i, result in enumerate(results, 1):
            print(f"Результат {i}:")
            print(f"Заголовок: {result['title']}")
            print(f"URL: {result['url']}")
            print("\nСодержание:")
            print("-" * 80)
            print(result['content'])
            print("-" * 80)
            print()

    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()