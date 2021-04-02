from preprocessing.branch_graph import get_character_branch_graph_leftside, get_word_branch_graph_rightside, get_character_branch_graph_rightside, get_word_branch_graph_leftside

import numpy as np
from scipy.stats import entropy

def get_branch_score_dict(graph):
    stack_ = [(word, 1) for word in list(graph.keys()) if word != 'count']
    word_set = {}
    prev_words = []

    now_graph = graph
    now_step = 1
    while stack_:

        word, step = stack_.pop()

        if (step <= now_step):
            prev_words = prev_words[:step - 1]
            now_graph = graph
            for prev_word, st, cnt in prev_words:
                now_graph = now_graph[prev_word]

        now_step = step

        if (len(prev_words) < 1):
            prev_words.append((word, step, np.inf))
        elif (len(prev_words) == 1):
            score = entropy([now_graph[word][i]['count'] for i in now_graph[word].keys() if i != 'count'])
            prev_words.append((word, step, score))
            word_set[''.join(list(map(lambda x: x[0], prev_words)))] = score
        else:
            score = entropy([now_graph[word][i]['count'] for i in now_graph[word].keys() if i != 'count'])
            prev_words.append((word, step, score))
            word_set[''.join(list(map(lambda x: x[0], prev_words)))] = score
        if (len(list(now_graph[word].keys())) > 1):
            stack_.extend([(next_word, step + 1) for next_word in list(now_graph[word].keys()) if next_word != 'count'])
            now_graph = now_graph[word]
        else:
            continue

    return word_set


def get_branch_score_dict_slice(score, word_set):
    now_score = np.inf
    word_scores = {}
    for word in word_set:
        scores = []
        for idx in range(2, len(word) + 1):
            now_score = score[word[:idx]]
            scores.append(now_score)

        word_scores[word] = scores

    return word_scores

def word_branch_score_slice_index(scores, down_rate = 0.7, top_rate = 0.4):
    # 혹시 모르니까 가중치를 넣자
    is_word = len(scores)+1
    for idx in range(1,len(scores)):
        if(scores[idx] < scores[idx-1] * down_rate or scores[idx-1]*(1+top_rate) < scores[idx]):
            is_word = idx+1
            break
    return is_word


def word_branch_score_slice_index(scores, down_rate=0.7, top_rate=0.4):
    # 혹시 모르니까 가중치를 넣자
    is_word = len(scores) + 1
    if (sum(scores) < 0.1):
        return 0

    for idx in range(1, len(scores)):

        if (scores[idx] < scores[idx - 1] * down_rate or scores[idx - 1] * (1 + top_rate) < scores[idx]):
            is_word = idx + 1
            break

    return is_word

def get_word_from_branch_score(word_scores):
    words = list(word_scores.keys())

    meaningful_words = []

    for word in words:
        if (len(word) == 2):
            meaningful_words.append(word)
            continue
        else:
            meaningful_words.append(word[:word_branch_score_slice_index(word_scores[word])])

    return meaningful_words