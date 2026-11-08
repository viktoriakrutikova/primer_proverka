import re
FUNC_RE = re.compile(r"arcsin|arccos|arctan|log_\d+|log10|sin|cos|tan|cot|ln|log")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
LETTERS_RE = re.compile(r"[A-Za-z]+")

class ParseError(Exception):
    """Выражение записано неправильно."""
    pass


class Token:
    """Один кусочек выражения: число, буква, функция, оператор или скобка."""
    def __init__(self, kind, val, start, end, space):
        self.kind = kind    # num, var, const, func, op, lp, rp
        self.val = val      # сам текст токена
        self.start = start  # где начинается в тексте
        self.end = end      # где заканчивается в тексте
        self.space = space  # был ли пробел перед ним

def tokenize_runs(text):
    """Режет текст на цепочки токенов. Русские слова, запятые, точки,
    переносы строк и неизвестные символы разрывают цепочку."""
    runs = []       # готовые цепочки
    current = []    # цепочка, которую собираем сейчас
    space = False   # был ли пробел перед следующим токеном
    i = 0
    n = len(text)

    while i < n:
        c = text[i]
        brk = False  # нужно ли разорвать цепочку
        if c in " \t\r":
            space = True
            i += 1
            continue
        elif c == "\n":
            brk = True
            i += 1
        elif c.isdigit():
            m = NUM_RE.match(text, i)
            current.append(Token("num", m.group(), i, m.end(), space))
            i = m.end()
            space = False
        elif c.isascii() and c.isalpha():
            func = FUNC_RE.match(text, i)
            word = LETTERS_RE.match(text, i).group()
            after_func_is_letter = bool(func) and func.end() < n and \
                text[func.end()].isascii() and text[func.end()].isalpha()

            if func and not after_func_is_letter:
                current.append(Token("func", func.group(), i, func.end(), space))
                i = func.end()
                space = False
            elif func or len(word) > 3:
                # длинное слово или "since" - это обычный текст
                brk = True
                i += len(word)
            elif word == "pi":
                current.append(Token("const", "pi", i, i + 2, space))
                i += 2
                space = False
            else:
                # короткое слово: каждая буква - отдельная переменная (2ab = 2*a*b)
                for k, letter in enumerate(word):
                    sp = space if k == 0 else False
                    current.append(Token("var", letter, i + k, i + k + 1, sp))
                i += len(word)
                space = False

        elif c in "+-*/^":
            # "- " или "* " в начале строки - это маркер списка, а не оператор
            if not current and c in "-*+" and i + 1 < n and text[i + 1] in " \t":
                i += 1
            else:
                current.append(Token("op", c, i, i + 1, space))
                i += 1
                space = False

        elif c == "(":
            current.append(Token("lp", c, i, i + 1, space))
            i += 1
            space = False

        elif c == ")":
            current.append(Token("rp", c, i, i + 1, space))
            i += 1
            space = False

        else:
            brk = True
            i += 1

        if brk:
            if current:
                runs.append(current)
            current = []
            space = False

    if current:
        runs.append(current)
    return runs

class Parser:
    """Проверяет, что цепочка токенов - правильно записанное выражение.
    Если нет - бросает ParseError."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Посмотреть следующий токен, не забирая его."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def take(self):
        """Забрать следующий токен."""
        if self.pos >= len(self.tokens):
            raise ParseError("выражение оборвалось")
        self.pos += 1
        return self.tokens[self.pos - 1]

    def next_is_op(self, ops):
        t = self.peek()
        return t is not None and t.kind == "op" and t.val in ops

    def parse(self):
        self.expr()
        if self.pos != len(self.tokens):
            raise ParseError("лишние символы")

    def expr(self):                    # a + b - c
        self.term()
        while self.next_is_op("+-"):
            self.take()
            self.term()
    def term(self):                    # a * b, a / b, 3x
        self.unary()
        while True:
            t = self.peek()
            if t is None:
                break
            if self.next_is_op("*/"):
                self.take()
                self.unary()
            elif not t.space and t.kind in ("var", "const", "func", "lp"):
                self.power()           # неявное умножение: 3x, 2ab, 5sin(x)
            else:
                break

    def unary(self):                   # -x
        if self.next_is_op("+-"):
            self.take()
            self.unary()
        else:
            self.power()

    def power(self):                   # a^b
        self.atom()
        if self.next_is_op("^"):
            self.take()
            self.unary()

    def atom(self):
        t = self.take()
        if t.kind in ("num", "var", "const"):
            return
        if t.kind == "lp":             # (выражение)
            self.expr()
            self.close()
            return
        if t.kind == "func":
            nxt = self.peek()
            if nxt is not None and nxt.kind == "lp":              # sin(x)
                self.take()
                self.expr()
                self.close()
            elif nxt is not None and nxt.kind in ("num", "var", "const"):  # sin x
                self.take()
            else:
                raise ParseError("у функции нет аргумента")      # например 3cos
            return
        raise ParseError("неожиданный символ " + t.val)

    def close(self):
        if self.take().kind != "rp":
            raise ParseError("нет закрывающей скобки")

def whole_thing_in_brackets(tokens):
    """True для выражений вида (2x + pi) - всё целиком в одних скобках."""
    if tokens[0].kind != "lp":
        return False
    depth = 0
    for i in range(len(tokens)):
        if tokens[i].kind == "lp":
            depth += 1
        elif tokens[i].kind == "rp":
            depth -= 1
            if depth == 0:
                return i == len(tokens) - 1
    return False


def is_interesting(tokens):
    """Отсеивает правильные, но неинтересные выражения."""
    # 5 + 2 - нет ни одной переменной
    if not any(t.kind == "var" for t in tokens):
        return False

    # a * b, ab, x / y - только буквы и * или /
    only_letters_and_mul = True
    for t in tokens:
        is_letter = t.kind == "var"
        is_mul = t.kind == "op" and t.val in "*/"
        if not (is_letter or is_mul):
            only_letters_and_mul = False
    if only_letters_and_mul:
        return False

    # (2x + pi) - всё в одних скобках
    if whole_thing_in_brackets(tokens):
        return False

    # sin x и sin(x) - функция с простым аргументом
    if tokens[0].kind == "func":
        if len(tokens) == 2:
            return False
        if len(tokens) == 4 and tokens[1].kind == "lp":
            return False

    return True
def find_math_expressions(text):
    """Возвращает список математических выражений, найденных в тексте."""
    result = []
    for run in tokenize_runs(text):
        try:
            Parser(run).parse()
        except ParseError:
            continue
        if is_interesting(run):
            expr = text[run[0].start:run[-1].end]
            if expr not in result:
                result.append(expr)
    return result
