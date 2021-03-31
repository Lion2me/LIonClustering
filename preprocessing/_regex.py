import re

korean_jamo_pattern = re.compile('[ㄱ-ㅎㅏ-ㅠ/-]')

doublespace_pattern = re.compile('\s+')

korean_pattern = re.compile('[가-힣]')

english_pattern = re.compile('[a-zA-Z]')

mean_ful_reg = re.compile('[^가-힣a-zA-Z\s]+')

double_space = re.compile('[\s]+')
