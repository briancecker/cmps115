"""
Taken from https://github.com/davidadamojr/TextRank and ported to python3

_from this paper: https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf

_external dependencies: nltk, numpy, networkx

_based on https://gist.github.com/voidfiles/1646117
"""

import itertools
import networkx as nx
import nltk
from main.models import Transcripts, Utterances, Tokens


def _filter_for_tags(tagged, pos_prefixes=("NN", "VB", "JJ")):
    results = list()
    for item in tagged:
        for pat in pos_prefixes:
            if item[1].startswith(pat):
                results.append(item)
                break

    return results


def _normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def _unique_everseen(iterable, key=None):
    """
    List unique elements, preserving order. Remember all elements ever seen.
     unique_everseen('_a_a_a_a_b_b_b_c_c_d_a_a_b_b_b') --> _a _b _c _d
     unique_everseen('_a_b_b_cc_a_d', str.lower) --> _a _b _c _d
    Args:
        iterable:
        key:

    Returns:

    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def _l_distance(first_string, second_string):
    """
    function to find the levenshtein distance between two words/sentences - gotten from
    http://rosettacode.org/wiki/_levenshtein_distance#_python"
    Args:
        first_string:
        second_string:

    Returns:

    """
    if len(first_string) > len(second_string):
        first_string, second_string = second_string, first_string
    distances = list(range(len(first_string) + 1))
    for index2, char2 in enumerate(second_string):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(first_string):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]


def _build_graph(nodes):
    """

    Args:
        nodes: list of hashables that represents the nodes of the graph

    Returns:

    """
    gr = nx.Graph()
    # gr = nx._graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    node_pairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by levenshtein distance)
    for pair in node_pairs:
        first_string = pair[0]
        second_string = pair[1]
        lev_distance = _l_distance(first_string, second_string)
        gr.add_edge(first_string, second_string, weight=lev_distance)

    return gr


def _extract_keyphrases(tokens, num_keyphrases):
    """
    Extract kephrases and/or words from the text.
    Args:
        tokens: A list of tokens from the text
        num_keyphrases: The number of key phrases to extract. If an integer, takes the exact number. If a float,
                        takes num_keyphrases as the percentage of the total vertices.

    Returns: A list of key phrases and/or words

    """

    # assign _p_o_s tags to the words in the text
    tagged = nltk.pos_tag(tokens)
    textlist = [x[0] for x in tagged]

    tagged = _filter_for_tags(tagged)
    tagged = _normalize(tagged)

    unique_word_set = _unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)

    # this will be used to determine adjacent words in order to construct keyphrases with two words

    graph = _build_graph(word_set_list)

    # page_rank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = nx.pagerank(graph, weight='weight')

    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

    # the number of keyphrases returned will be relative to the size of the text (a third of the number of vertices)
    if type(num_keyphrases) is int:
        keyphrases = keyphrases[:num_keyphrases]
    elif type(num_keyphrases) is float:
        keyphrases = keyphrases[:int(len(keyphrases) * num_keyphrases)]
    else:
        raise ValueError("summary_length is of type {0}. Expected int or float.".format(type(num_keyphrases)))

    # take keyphrases with multiple words into consideration as done in the paper - if two words are adjacent in the
    # text and are selected as keywords, join them together
    modified_keyphrases = set([])
    dealt_with = set([])  # keeps track of individual keywords that have been joined to form a keyphrase
    i = 0
    j = 1
    while j < len(textlist):
        first_word = textlist[i]
        second_word = textlist[j]
        if first_word in keyphrases and second_word in keyphrases:
            keyphrase = first_word + ' ' + second_word
            modified_keyphrases.add(keyphrase)
            dealt_with.add(first_word)
            dealt_with.add(second_word)
        else:
            if first_word in keyphrases and first_word not in dealt_with:
                modified_keyphrases.add(first_word)

            # if this is the last word in the text, and it is a keyword,
            # it definitely has no chance of being a keyphrase at this point
            if j == len(textlist) - 1 and second_word in keyphrases and second_word not in dealt_with:
                modified_keyphrases.add(second_word)

        i += 1
        j += 1

    return modified_keyphrases


def key_phrases(video, num_keyphrases):
    """
    Extract n keywords from the video based on transcripts. Uses tokens if they exist, otherwise tokenizes the
    transcript text using nltk.
    Args:
        video: A Videos database entry
        num_keyphrases: The number of key phrases to extract. If an integer, takes the exact number. If a float,
                        takes num_keyphrases as the percentage of the total vertices.

    Returns: A list of key words
    """
    transcript = Transcripts.objects.filter(video_id=video.id).all()
    if len(transcript) == 0:
        return []
    transcript = transcript[0]
    utterances = Utterances.objects.filter(transcript_id=transcript.id).all()
    tokens = list()
    for utterance in utterances:
        tokens += Tokens.objects.filter(utterance_id=utterance.id).all()

    text_tokens = [token.text for token in tokens]
    return _extract_keyphrases(text_tokens, num_keyphrases)


def summarize(video, summary_length):
    """
    Summarize a video based on the utterances in its transcript
    Args:
        video: A Videos database entry
        summary_length: The length of the summary. If an integer, then it is taken as an exact number of utterances.
                        If a float, then it is taken as a percentage of the total utterances.

    Returns: A text summary of the video
    """
    transcript = Transcripts.objects.filter(video_id=video.id).all()
    if len(transcript) == 0:
        return ""
    transcript = transcript[0]
    utterances = Utterances.objects.filter(transcript_id=transcript.id).all()

    graph = _build_graph(utterances)
    calculated_page_rank = nx.pagerank(graph, weight='weight')

    # most important sentences in ascending order of importance
    sentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

    # make the summary
    if type(summary_length) == int:
        # Exact number of utterances
        return sentences[:summary_length].join(" ")
    elif type(summary_length) == float:
        # Percentage of total utterances
        return sentences[:int(len(sentences) * summary_length)].join(" ")
    else:
        raise ValueError("summary_length is of type {0}. Expected int or float.".format(type(summary_length)))
