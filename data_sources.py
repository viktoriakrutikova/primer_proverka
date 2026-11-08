import requests

def get_from_console():
    return input("Введите текст с математическими выражениями: ")

def get_from_file(filename=None):
    """Принимает имя файла как аргумент. Если не передано — спрашивает через input."""
    if not filename:
        filename = input("Введите имя файла (например, text.txt): ").strip()
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return ""

def get_from_url(url=""):
    if not url:
        url = input("Введите URL страницы (например, https://example.com): ").strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return ""