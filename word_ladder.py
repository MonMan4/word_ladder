#!/bin/python3

from collections import deque


def word_ladder(start_word, end_word, dictionary_file='words5.dict'):
    '''
    Returns a list satisfying the following properties:

    1. the first element is `start_word`
    2. the last element is `end_word`
    3. elements at index i and i+1 are `_adjacent`
    4. all elements are entries in the `dictionary_file` file

    Returns None if no ladder exists.
    '''
    # Trivial case: start equals end
    if start_word == end_word:
        return [start_word]

    # Load the dictionary as a set for O(1) membership and deletion.
    with open(dictionary_file) as f:
        dictionary = set(line.strip() for line in f)

    # The start word must be allowed as a step in the ladder.
    # (It's already in the stack, so remove it from the dictionary
    #  to prevent cycles that revisit the start.)
    dictionary.discard(start_word)

    # Queue of partial ladders (each is a list used as a stack).
    queue = deque()
    queue.append([start_word])

    while queue:
        stack = queue.popleft()
        top = stack[-1]

        # Find every unused dictionary word adjacent to `top`.
        # NOTE: we build a list of removals so we don't mutate
        # the set while iterating over it.
        to_remove = []
        for word in dictionary:
            if _adjacent(word, top):
                if word == end_word:
                    return stack + [word]
                to_remove.append(word)
                # Copy the stack — do NOT reuse `stack`.
                new_stack = stack + [word]
                queue.append(new_stack)

        for word in to_remove:
            dictionary.discard(word)

    return None

def verify_word_ladder(ladder):
    '''
    Returns True if each entry of the input list is adjacent to its neighbors;
    otherwise returns False.

    >>> verify_word_ladder(['stone', 'shone', 'phone', 'phony'])
    True
    >>> verify_word_ladder(['stone', 'shone', 'phony'])
    False
    '''
    if not ladder:
        return False
    for i in range(len(ladder) - 1):
        if not _adjacent(ladder[i], ladder[i+1]):
            return False
    return True

def _adjacent(word1, word2):
    '''
    Returns True if the input words differ by only a single character;
    returns False otherwise.

    >>> _adjacent('phone','phony')
    True
    >>> _adjacent('stone','money')
    False
    '''
    if len(word1) != len(word2):
        return False
    diffs = 0
    for a, b in zip(word1, word2):
        if a != b:
            diffs += 1
            if diffs > 1:
                return False
    return diffs == 1
