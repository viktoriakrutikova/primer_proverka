
import unittest
from parser import find_math_expressions, is_syntactically_correct


class TestParserSyntax(unittest.TestCase):
    """Проверка синтаксиса математических выражений."""

    def check(self, exprs, expected):
        for expr in exprs:
            with self.subTest(expr=expr):
                self.assertEqual(is_syntactically_correct(expr), expected)

    def test_valid_algebraic_expressions(self):
        self.check([
            "3x+5",
            "a^2+2ab+b^2",
            "5a^3-2a+7",
            "(x - 3) * (x + 4)",
            "2 * x^4 - 5x^2 + 10"
        ], True)

    def test_valid_trigonometric_expressions(self):
        self.check([
            "sin(x)+cos(x)",
            "2sin(x)-3cos(x)",
            "tan(x)+cot(x)",
            "5sin(2x+pi)",
            "sin(x)^2+cos(x)^2",
            "arcsin(x)+arccos(x)"
        ], True)

    def test_valid_logarithms_and_powers(self):
        self.check([
            "log_2(x+1)",
            "ln(x^2+1)",
            "2^x+3",
            "e^-x",
            "e^(-x)",
            "log10(x) * ln(x)"
        ], True)

    def test_valid_fractions_and_decimals(self):
        self.check([
            "5/6",
            "667/78676+6861761/1898",
            "5.364 * y",
            "1,5 + 2,5",
            "-1000-1000",
            "-2.5+3.7"
        ], True)

    def test_invalid_expressions(self):
        self.check([
            "999",
            "",
            "sin(x))",
            "(a + b",
            "((x + 1]",
            "{a + b)",
            "3x +",
            "a * b -",
            "log(, x)",
            "x ^"
        ], False)


class TestTextExtraction(unittest.TestCase):
    """Проверка поиска выражений в тексте."""

    def test_extract_algebra(self):
        text = """
        Рассмотрим многочлен 5a^3-2a+7
        и линейную функцию 3x+5.
        """

        result = find_math_expressions(text)

        self.assertIn("3x+5", result)
        self.assertIn("5a^3-2a+7", result)

    def test_extract_trigonometry(self):
        text = """
        sin(x)+cos(x)
        tan(x)+cot(x)
        5sin(2x+pi)
        arcsin(x)+arccos(x)
        """

        result = find_math_expressions(text)

        self.assertIn("sin(x)+cos(x)", result)
        self.assertIn("tan(x)+cot(x)", result)
        self.assertIn("5sin(2x+pi)", result)
        self.assertIn("arcsin(x)+arccos(x)", result)

    def test_extract_fractions_and_negative_numbers(self):
        text = """
        -1000-1000
        667/78676+6861761/1898
        """

        result = find_math_expressions(text)

        self.assertIn("-1000-1000", result)
        self.assertIn("667/78676+6861761/1898", result)

    def test_extract_logarithms(self):
        text = """
        ln(x^2+1)
        log10(x) * ln(x)
        """

        result = find_math_expressions(text)

        self.assertIn("ln(x^2+1)", result)
        self.assertIn("log10(x) * ln(x)", result)

    def test_remove_duplicates(self):
        text = """
        3x+5
        3x+5
        sin(x)+cos(x)
        sin(x)+cos(x)
        """

        result = find_math_expressions(text)

        self.assertEqual(result.count("3x+5"), 1)
        self.assertEqual(result.count("sin(x)+cos(x)"), 1)

    def test_empty_text(self):
        text = "Обычный текст без математических выражений."

        self.assertEqual(find_math_expressions(text), [])


if __name__ == "__main__":
    unittest.main()
