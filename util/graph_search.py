from preprocessing.word_branch_graph import get_character_branch_graph_leftside, get_word_branch_graph_rightside, get_character_branch_graph_rightside, get_word_branch_graph_leftside

def get_none_character_from_graph(graph):
    stack_ = [(word, 1) for word in list(graph.keys()) if word != 'count']
    prev_words = []

    now_graph = graph
    now_step = 1
    while stack_:

        word, step = stack_.pop()

        if (step <= now_step):
            prev_words = prev_words[:step - 1]
            now_graph = graph
            for prev_word, st in prev_words:
                now_graph = now_graph[prev_word]

        now_step = step

        prev_words.append((word, step))
        if (len(list(now_graph[word].keys())) > 1):
            stack_.extend([(next_word, step + 1) for next_word in list(now_graph[word].keys()) if next_word != 'count'])
            now_graph = now_graph[word]
        else:
            continue
