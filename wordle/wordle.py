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
    ).pivot(index='guess', columns='solution', values='score')

    return df


class Wordle:
    def __init__(self, wordlist=None, scoredf=None, solution=None):
        assert not (wordlist is None and scoredf is None)
        if scoredf is not None:
            assert scoredf.index.size == scoredf.columns.size

            self.wordlist = list(scoredf.index)
            self.scoredf = scoredf

        else:
            self.wordlist = list(wordlist)
            self.scoredf = compute_all_scores(self.wordlist)

        self.reset(solution)
        return

    def reset(self, solution=None):
        if solution is None:
            solution = random.choice(self.wordlist)
        self.solution = solution
        self.solution_space = list(self.wordlist)
        return

    def guess(self, word, score=None):
        if score is None:
            score = self.scoredf.loc[word, self.solution]
            
        mask = self.scoredf.loc[word, self.solution_space] == score
        self.solution_space = (
            self.scoredf
            .loc[word, self.solution_space]
            .index[mask]
            .to_list()
        )
        
        return score

    def suggest(self, solution_space=None):
        if solution_space is None:
            solution_space = self.solution_space

        if len(solution_space) == 1:
            return solution_space[0]

        scores = (
            self.scoredf[solution_space]
            .apply(lambda x: x.value_counts().mean(), axis=1)
            .rename('scores')
            .to_frame()
        )
        scores['in_solution_space'] = scores.index.isin(solution_space)
        guess = scores.sort_values(
            by=['scores', 'in_solution_space'],
            ascending=[True, False]
        ).index[0]

        return guess