import os
import unittest
from data_sources import get_from_file


class TestDataSourcesSimple(unittest.TestCase):

    def test_get_from_existing_file(self):
        """Создаем временный файл, читаем его через функцию и удаляем."""
        test_filename = "пример.txt"
        with open(test_filename, "w", encoding="utf-8") as f:
            f.write("Тест: 3x+5 и sin x + cos x")

        try:
            content = get_from_file(test_filename)
            self.assertIn("3x+5", content)
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)

    def test_get_from_missing_file(self):
        """Проверяем поведение, если файла не существует."""
        content = get_from_file("nonexistent_file_12345.txt")
        self.assertEqual(content, "")


if __name__ == "__main__":
    unittest.main()