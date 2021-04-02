import os
import json
import pandas as pd
import re
from collections import defaultdict
from _regex import mean_ful_reg, double_space_reg


# list of str input
def get_character_branch_graph_leftside(texts):
    dict_ = defaultdict()

    words = ' '.join([re.sub(mean_ful_reg, ' ', st) for st in texts])
    words = re.sub(double_space_reg, ' ', words).split(' ')

    for word in words:
        now_dict_p = dict_
        for i in word:
            if i in now_dict_p.keys():
                now_dict_p[i]['count'] += 1
                now_dict_p = now_dict_p[i]
            else:
                now_dict_p[i] = defaultdict()
                now_dict_p[i]['count'] = 1
                now_dict_p = now_dict_p[i]

    return dict_


# list of str input
def get_character_branch_graph_rightside(texts):
    dict_ = defaultdict()

    words = ' '.join([re.sub(mean_ful_reg, ' ', st) for st in texts])
    words = re.sub(double_space_reg, ' ', words).split(' ')

    for word in words:
        now_dict_p = dict_
        for i in word[::-1]:
            if i in now_dict_p.keys():
                now_dict_p[i]['count'] += 1
                now_dict_p = now_dict_p[i]
            else:
                now_dict_p[i] = defaultdict()
                now_dict_p[i]['count'] = 1
                now_dict_p = now_dict_p[i]

    return dict_


def get_word_branch_graph_leftside(texts):
    dict_ = defaultdict()

    texts = [re.sub(mean_ful_reg, ' ', st) for st in texts]
    texts = [re.sub(double_space_reg, ' ', st).split(' ') for st in texts]

    for text in texts:
        now_dict_p = dict_
        for word in text:
            if word in now_dict_p.keys():
                now_dict_p[word]['count'] += 1
                now_dict_p = now_dict_p[word]
            else:
                now_dict_p[word] = defaultdict()
                now_dict_p[word]['count'] = 1
                now_dict_p = now_dict_p[word]

    return dict_


def get_word_branch_graph_rightside(texts):
    dict_ = defaultdict()

    texts = [re.sub(mean_ful_reg, ' ', st) for st in texts]
    texts = [re.sub(double_space_reg, ' ', st).split(' ') for st in texts]

    for text in texts:
        now_dict_p = dict_
        for word in text[::-1]:
            if word in now_dict_p.keys():
                now_dict_p[word]['count'] += 1
                now_dict_p = now_dict_p[word]
            else:
                now_dict_p[word] = defaultdict()
                now_dict_p[word]['count'] = 1
                now_dict_p = now_dict_p[word]

    return dict_



