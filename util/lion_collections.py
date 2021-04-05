from collections import defaultdict , Counter
from copy import copy
from functools import reduce
from scipy.sparse import csr_matrix

# 리스트 단위로 CountVectorize를 하면?

def LionCounter(*args, **kwargs):
    if (len(args) < 1):
        print('error')
        return

    deep = False
    return_type = 'list'

    if ('deep' in kwargs.keys() and kwargs['deep'] == True):
        deep = True
    if ('return_type' in kwargs.keys() and kwargs['return_type'] == 'csr'):
        return_type = 'csr'
        return_csr = []

    all_Count_Vector = defaultdict(int)

    word_set = sorted(' '.join(list(reduce(lambda x, y: x + y, args))).split(' '))

    all_Count_Vector = Counter(word_set)

    word_set = list(set(word_set))

    dict_template = defaultdict(int, {key: 0 for key in word_set})

    if deep == False:
        args_dicts = [copy(dict_template) for idx in range(len(args))]
        for idx in range(len(args)):
            args_dicts[idx].update(Counter(' '.join(args[idx]).split(' ')))
    else:
        sents = list(reduce(lambda x, y: x + y, args))
        args_dicts = [copy(dict_template) for idx in range(len(sents))]
        for idx in range(len(sents)):
            args_dicts[idx].update(Counter(sents[idx].split(' ')))

    if (return_type == 'csr'):
        return {'words': word_set, '부분': csr_matrix([list(args_dict.values()) for args_dict in args_dicts]),
                '전체': csr_matrix(list(all_Count_Vector.values()))}
    elif (return_type == 'list'):
        return {'words': word_set, '부분': args_dicts, '전체': all_Count_Vector}