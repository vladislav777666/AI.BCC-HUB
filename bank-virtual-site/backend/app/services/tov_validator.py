from typing import Dict
import re

def validate_tov(text: str) -> Dict:
    violations = []
    length = len(text)
    if not 180 <= length <= 220:
        violations.append("length")
    emoji_count = len(re.findall(r'[\U0001F000-\U0001FFFF]', text))
    if emoji_count > 1:
        violations.append("emoji")
    return {"length": length, "emoji": emoji_count, "violations": violations}