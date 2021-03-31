from _check import is_jamo_korean , is_korean, is_english
from soynlp.hangle import decompose,compose

def sentence_to_jamo(sent):

    def transform(char):
        if char == ' ':
            return char
        # 자모로 자르는 데 문제는 영어일 경우
        if(is_korean(char)):
            cjj = decompose(char)
        elif(is_english(char)):
            cjj = (char)
        else:
            return (' ')
        if len(cjj) == 1:
            return cjj
        cjj_ = ''.join(c if c != ' ' else '-' for c in cjj)
        return cjj_
    sent_ = ''.join(transform(char) for char in sent)
    sent_ = doublespace_pattern.sub(' ', sent_)
    return sent_

def jamo_to_word(jamo):
  # idx를 기반으로 순차접근 방식으로 접근하면서 저는 소스가 흐트러졌는데 깔끔합니다.
    jamo_list, idx = [], 0
    word = ""
    while idx < len(jamo):
        if not is_jamo_korean(jamo[idx]):
            jamo_list.append(jamo[idx])
            idx += 1
        else:
            jamo_list.append(jamo[idx:idx + 3])
            idx += 3
            word = ""
    for jamo_char in jamo_list:
        if len(jamo_char) == 1:
            word += jamo_char
        elif jamo_char[2] == "-":
            word += compose(jamo_char[0], jamo_char[1], " ")
        else:
            word += compose(jamo_char[0], jamo_char[1], jamo_char[2])
    return word

def jamo_to_word_sent(sent_jamo):
    sent = ""
    idx = 0
    while idx < len(sent_jamo)-1:
#        print(sent_jamo[idx:idx+3])
#        print(is_jamo_korean(sent_jamo[idx]))
        if(is_jamo_korean(sent_jamo[idx])) :
            sent+=jamo_to_word(sent_jamo[idx:idx+3])
            idx = idx+3
        else:
            sent+=jamo_to_word(sent_jamo[idx:idx+1])
            idx = idx+1
        print(sent)
    return sent
