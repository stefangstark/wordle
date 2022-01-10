import random
import pandas as pd
import numpy as np
from wordle.utils import compute_all_scores
from tqdm.auto import tqdm
from pathlib import Path
import json
from wordle.utils import load_words


class Wordle:
    def __init__(self, wordlist=None, scoredf=None, solution=None):
        assert not (wordlist is None and scoredf is None)
        if scoredf is not None:
            self.wordlist = list(scoredf.index)
            self.scoredf = scoredf

        else:
            self.wordlist = list(wordlist)
            self.scoredf = compute_all_scores(self.wordlist)

        assert np.array_equal(self.scoredf.index.values, self.wordlist)
        assert np.array_equal(self.scoredf.columns.values, self.wordlist)

        self.reset(solution)
        return

    def reset(self, solution=None):
        '''Reset game with a solution'''
        if solution is None:
            solution = random.choice(self.wordlist)
        self.solution = solution
        self.solution_space = list(self.wordlist)
        return

    def guess(self, word, score=None):
        '''Guess and resrict solution space to consistent words.'''
        if score is None:
            score = self.scoredf.loc[word, self.solution]

        # Restrict solution space to all words that yield the same score
        mask = self.scoredf.loc[word, self.solution_space] == score
        self.solution_space = (
            self.scoredf
            .loc[word, self.solution_space]
            .index[mask]
            .to_list()
        )

        return score

    def suggest(self, solution_space=None):
        '''Suggests the best word to guess next.'''
        if solution_space is None:
            solution_space = self.solution_space

        if len(solution_space) == 1:
            return solution_space[0]

        # The best word reduces the search space the most (on average)
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


def compute_all_second_suggestions(game, first_guess=None):
    def iterate(scores):
        groupby = scores.groupby(scores)
        items = tqdm(
                groupby.groups.items(),
                desc='Computing second guesses')

        for key, solution_space in items:
            yield key, game.suggest(solution_space)

    if first_guess is None:
        first_guess = game.suggest(game.wordlist)

    scores = game.scoredf.loc[first_guess]

    return dict(iterate(scores))


def cache_state(kind, cachedir):
    words = load_words(kind=kind)
    scoredf = compute_all_scores(words)

    game = Wordle(scoredf=scoredf)
    first_guess = game.suggest()
    second_guesses = compute_all_second_suggestions(game, first_guess)

    cachedir.mkdir(exist_ok=True, parents=True)
    Path(cachedir/'words.txt').write_text('\n'.join(words))
    scoredf.to_csv(cachedir/'scoredf.csv', index_label='')
    Path(cachedir/'first_guess.txt').write_text(first_guess)
    json.dump(second_guesses, open(cachedir/'second_guesses.json', 'w'))

    return scoredf, first_guess, second_guesses


def load_state(kind, cachedir):
    try:
        scoredf = pd.read_csv(cachedir/'scoredf.csv', index_col=0)
        first_guess = Path(cachedir/'first_guess.txt').read_text().strip()
        second_guesses = json.load(open(cachedir/'second_guesses.json'))

    except OSError:
        scoredf, first_guess, second_guesses = cache_state(kind, cachedir)

    game = Wordle(scoredf=scoredf)
    return game, first_guess, second_guesses
