import re

korean_jamo_pattern = re.compile('[ㄱ-ㅎㅏ-ㅠ/-]')

doublespace_pattern = re.compile('\s+')

korean_pattern = re.compile('[가-힣]')

english_pattern = re.compile('[a-zA-Z]')

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
