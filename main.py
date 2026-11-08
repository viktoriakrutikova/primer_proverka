from parser import find_math_expressions
from data_sources import get_from_console, get_from_file, get_from_url

def main():
    print("--- Поиск и проверка математических выражений (Слоистая архитектура) ---")
    print("1. Ввод текста с клавиатуры")
    print("2. Поиск в файле")
    print("3. Поиск по URL")

    choice = input("Выберите режим (1, 2 или 3): ").strip()

    raw_text = ""

    if choice == "1":
        raw_text = get_from_console()
    elif choice == "2":
        raw_text = get_from_file()
    elif choice == "3":
        raw_text = get_from_url()
    else:
        print("Неверный выбор режима.")
        return

    if raw_text:
        results = find_math_expressions(raw_text)
        print("\nКорректные выражения:")
        for expr in results:
            print(f"- {expr}")


if __name__ == "__main__":
    main()