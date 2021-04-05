import numpy as np
from util.lion_collections import LionCounter
from soynlp.word import pmi

def LionRelativeAppearanceRatio(*args):
    Counters_ = LionCounter(*args)

    words = list(Counters_['전체'].keys())
    max_count = np.array(list(Counters_['전체'].values()))

    appearance_ratio = []

    for idx in range(len(args)):
        appearance_ratio.append(np.array(list(Counters_['부분'][idx].values())) / max_count)

    return appearance_ratio

# 미완
def PMI(*args):
    Counters_ = LionCounter(*args, deep=True, return_type='csr')

    return {'words': Counters_['words'], 'pmi': pmi(Counters_['부분'])}