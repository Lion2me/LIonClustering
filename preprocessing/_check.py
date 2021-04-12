import re
from preprocessing._regex import korean_pattern, english_pattern, korean_jamo_pattern

def is_korean(char):
    if korean_pattern.match(char):
        return True
    else:
        return False


def is_english(char):
    if english_pattern.match(char):
        return True
    else:
        return False

def is_jamo_korean(char):
    if korean_jamo_pattern.match(char):
        return True
    else:
        return False
