import os
import json
import pandas as pd
import re
from collections import defaultdict
from _regex import mean_ful_reg, double_space_reg

def get_character_branch_graph_leftside(texts):
    dict_ = defaultdict()

    text = ' '.join([' '.join(texts) for i in range(len(texts))])

    text = re.sub(mean_ful_reg, ' ', text)
    text = re.sub(double_space_reg, ' ', text)

    words = text.split(' ')

    for word in words:
        now_dict_p = dict_
        for i in word:
            if i in now_dict_p:
                now_dict_p['count'] += 1
                now_dict_p = now_dict_p[i]
            else:
                now_dict_p[i] = defaultdict()
                now_dict_p['count'] = 1
                now_dict_p = now_dict_p[i]

    return dict_


def get_character_branch_graph_rightside(texts):
    dict_ = defaultdict()

    text = ' '.join([' '.join(texts) for i in range(len(texts))])

    text = re.sub(mean_ful_reg, ' ', text)
    text = re.sub(double_space_reg, ' ', text)

    words = text.split(' ')

    for word in words:
        now_dict_p = dict_
        for i in word[::-1]:
            if i in now_dict_p:
                now_dict_p['count'] += 1
                now_dict_p = now_dict_p[i]
            else:
                now_dict_p[i] = defaultdict()
                now_dict_p['count'] = 1
                now_dict_p = now_dict_p[i]

    return dict_

