from collections import defaultdict , Counter
from copy import copy
from functools import reduce

def LionCounter(*args):
    all_Count_Vector = defaultdict(int)

    word_set = sorted(' '.join(list(reduce(lambda x, y: x + y, args))).split(' '))

    dict_template = defaultdict(int, {key: 0 for key in word_set})

    args_dicts = [copy(dict_template) for idx in range(len(args))]

    all_Count_Vector = Counter(word_set)

    for idx in range(len(args)):
        args_dicts[idx].update(Counter(' '.join(args[idx]).split(' ')))

    return {'부분': args_dicts, '전체': all_Count_Vector}