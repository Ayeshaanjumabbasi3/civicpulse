import re


INJECTION = re.compile(r"ignore\s+(all|any|the)\s+previous|system\s+prompt|developer\s+message|reveal\s+your\s+instructions", re.I)


def guard_text(value: str) -> str:
    if not INJECTION.search(value):
        return value
    return INJECTION.sub('[untrusted instruction removed]', value)
