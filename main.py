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
    simple_pattern = (
        r"\b(?:\d+|[a-zA-Z])\s*[\+\-\*/]\s*(?:\d+|[a-zA-Z])(?:\s*[\+\-\*/]\s*(?:\d+|[a-zA-Z]))*\b"
    )
    return re.findall(simple_pattern, text)