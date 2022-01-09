import pandas as pd
from itertools import product


def score_guess(solution, guess):
    yellows = set(solution)

    def iterate():
        for lhs, rhs in zip(solution, guess):
            if lhs == rhs:
                yield 'g'
            elif rhs in yellows:
                yield 'y'
            else:
                yield 'r'

    return ''.join(iterate())


def compute_all_scores(words):
    def iterate():
        for solution, guess in product(words, words):
            score = score_guess(solution, guess)
            yield solution, guess, score

    df = pd.DataFrame(
        iterate(),
        columns=['solution', 'guess', 'score']
    ).pivot(index='guess', columns='solution', values='score')

    return df


def load_words(kind='english_words'):
    if kind == 'english_words':
        from english_words import english_words_lower_alpha_set as words

    elif kind == 'nltk':
        from nltk.corpus import words
        words = words.words()
        words = filter(lambda x: x.islower() and x.isalpha(), words)

    else:
        raise ValueError

    words = sorted(set(filter(lambda x: len(x) == 5, words)))
    return words
