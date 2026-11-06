import re
import requests

def is_syntactically_correct(expr):
    expr = expr.strip()
    if not expr:
        return False

    stack = []
    for char in expr:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack:
                return False
            top = stack.pop()
            if (
                (char == ")" and top != "(")
                or (char == "}" and top != "{")
                or (char == "]" and top != "[")
            ):
                return False
    if stack:
        return False

    if re.search(r"[\+\-\*/\^,]\s*$", expr):
        return False

    if re.search(r"\(\s*,", expr) or re.search(r",\s*\)", expr):
        return False

    return True

def find_math_expressions(text):
    pattern = r"\b(?:[a-zA-Zа-яА-ЯёЁ]+\s*\([^)]*\)|\d+[a-zA-Z]*|[a-zA-Z]+\d*(?:\^\d+)?|\([^)]+\))(?:\s*[\+\-\*/\^]\s*(?:[a-zA-Zа-яА-ЯёЁ]+\s*\([^)]*\)|\d+[a-zA-Z]*|[a-zA-Z]+\d*(?:\^\d+)?|\([^)]+\)))*"
    candidates = re.findall(pattern, text)
    valid_expressions = [expr for expr in candidates if is_syntactically_correct(expr)]
    return list(set(valid_expressions))

def search_from_user_input():
    user_text = input("Введите текст с математическими выражениями: ")
    print("Корректные выражения:", find_math_expressions(user_text))