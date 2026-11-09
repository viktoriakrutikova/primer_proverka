import re

def is_syntactically_correct(expr):
    """Проверяет синтаксическую правильность математического выражения."""
    expr = expr.strip()
    if not expr:
        return False
    if not re.fullmatch(r"[a-zA-Z0-9_+\-*/^().,\s]+", expr):
        return False
    functions = (
        r"arcsin|arccos|log10|log_2|sin|cos|tan|cot|ln|log"
    )
    for match in re.finditer(
        rf"\b(?:{functions})\b", expr, re.IGNORECASE
    ):
        if not expr[match.end():].lstrip().startswith("("):
            return False
    balance = 0
    for char in expr:
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1

        if balance < 0:
            return False

    if balance != 0:
        return False
    if re.search(r"\(\s*\)|\(\s*,|,\s*\)", expr):
        return False
    if re.match(r"^[*/^]", expr):
        return False
    if re.search(r"[+\-*/^,]\s*$", expr):
        return False
    if not re.search(r"[+\-*/^]", expr):
        return False
    return True


def find_math_expressions(text):
    """Извлекает математические выражения из текста."""
    result = []
    seen = set()
    text = re.sub(r"\blog2(?=\s*\()", "log_2", text)
    number = r"\d+(?:[.,]\d+)?"
    function = (
        r"(?:arcsin|arccos|log10|log_2|sin|cos|tan|cot|ln|log)"
    )
    func_atom = (
        rf"(?:{number}\s*)?{function}\s*\([^()]*\)"
        rf"(?:\s*\^\s*\d+)?"
    )
    number_atom = (
        rf"{number}(?:/{number})?"
        rf"(?:\^\([^()]*\)|\^[+-]?[a-zA-Z0-9]+)?"
    )
    variable_atom = (
        rf"\d*[a-zA-Z]+"
        rf"(?:\^\([^()]*\)|\^[+-]?[a-zA-Z0-9]+)?"
    )
    group_atom = r"\([^()]*\)"
    atom = (
        rf"(?:{func_atom}|{number_atom}|"
        rf"{variable_atom}|{group_atom})"
    )
    expression_pattern = re.compile(
        rf"(?<![a-zA-Z0-9_])"
        rf"[+-]?\s*{atom}"
        rf"(?:\s*[\+\-*/^]\s*{atom})*"
        rf"(?![a-zA-Z0-9_])",
        re.IGNORECASE
    )
    function_pattern = re.compile(
        rf"(?<![a-zA-Z0-9_])"
        rf"(?:{number}\s*)?{function}\s*"
        rf"\([^()]*\)"
        rf"(?:\s*\^\s*\d+)?"
        rf"(?:\s*[\+\-*/^]\s*{atom})*",
        re.IGNORECASE
    )
    for line in text.splitlines():
        matches = []
        for match in function_pattern.finditer(line):
            matches.append(match)
        for match in expression_pattern.finditer(line):
            matches.append(match)
        matches.sort(key=lambda m: (m.start(), -len(m.group())))
        for match in matches:
            expr = match.group().strip()
            if is_syntactically_correct(expr):
                if expr not in seen:
                    result.append(expr)
                    seen.add(expr)

    return result
