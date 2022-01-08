from itertools import product
import pandas as pd
import random


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
    )

    return df


class Wordle:
    def __init__(self, wordlist, solution=None):
        self.wordlist = list(wordlist)
        self.scoredf = (
            compute_all_scores(self.wordlist)
            .pivot(index='guess', columns='solution', values='score')
        )
        self.reset(solution)
        return

    def reset(self, solution=None):
        if solution is None:
            solution = random.choice(self.wordlist)
        self.solution = solution
        self.solution_space = list(self.wordlist)
        return

    def guess(self, word):
        score = self.scoredf.loc[word, self.solution]
        mask = self.scoredf.loc[word, self.solution_space] == score
        self.solution_space = (
            self.scoredf
            .loc[word, self.solution_space]
            .index[mask]
            .to_list()
        )

        return score, len(self.solution_space)

    def suggest(self):
        return (
            self.scoredf[self.solution_space]
            .apply(lambda x: x.value_counts().mean(), axis=1)
            .idxmin()
        )

    def play(self):
        rounds = 0
        while len(self.solution_space) > 1:
            rounds = rounds + 1
            self.guess(self.suggest())

        return rounds
