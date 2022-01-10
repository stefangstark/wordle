import sys

import wordle
from pathlib import Path
from tqdm.auto import tqdm
import pandas as pd
import json

from wordle.wordle import Wordle


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


def cache(kind, cachedir):
    words = wordle.load_words(kind=kind)
    scoredf = wordle.compute_all_scores(words)

    game = wordle.Wordle(scoredf=scoredf)
    first_guess = game.suggest()
    second_guesses = compute_all_second_suggestions(game, first_guess)

    cachedir.mkdir(exist_ok=True,)
    Path(cachedir/'words.txt').write_text('\n'.join(words))
    scoredf.to_csv(cachedir/'scoredf.csv', index_label='')
    Path(cachedir/'first_guess.txt').write_text(first_guess)
    json.dump(second_guesses, open(cachedir/'second_guesses.json', 'w'))

    return words, scoredf, first_guess, second_guesses


def load(kind, cachedir):
    try:
        wordlist = Path(cachedir/'words.txt').read_text().splitlines()
        scoredf = pd.read_csv(cachedir/'scoredf.csv', index_col=0)
        first_guess = Path(cachedir/'first_guess.txt').read_text().strip()
        second_guesses = json.load(open(cachedir/'second_guesses.json'))

    except OSError:
        wordlist, scoredf, first_guess, second_guesses = cache(kind, cachedir)

    game = Wordle(scoredf=scoredf)
    return game, first_guess, second_guesses


def play(game, first_guess, second_guesses):
    rounds = 0
    guess = None
    score = None
    while guess != game.solution:
        rounds = rounds + 1
        if rounds == 1:
            guess = first_guess
        elif rounds == 2:
            guess = second_guesses[score]
        else:
            guess = game.suggest()

        score = game.guess(guess)

    return rounds


if __name__ == '__main__':
    wordlist_flavor = sys.argv[1] if len(sys.argv) > 1 else 'english_words'
    cachedir = Path(f'./cache/{wordlist_flavor}')
    game, first_guess, second_guesses = load(wordlist_flavor, cachedir)

    nrounds = dict()
    for word in tqdm(game.wordlist, desc='playing all games'):
        game.reset(word)
        nrounds[word] = play(game, first_guess, second_guesses)

    json.dump(nrounds, open(cachedir/'nrounds.json', 'w'))
