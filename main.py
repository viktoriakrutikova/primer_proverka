import re
import requests

def find_math_expressions(text):
    simple_pattern = (
        r"\b(?:\d+|[a-zA-Z])\s*[\+\-\*/]\s*(?:\d+|[a-zA-Z])(?:\s*[\+\-\*/]\s*(?:\d+|[a-zA-Z]))*\b"
    )
    return re.findall(simple_pattern, text)