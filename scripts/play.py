import sys
from pathlib import Path
from wordle import load_state

wordlist_flavor = sys.argv[1] if len(sys.argv) > 1 else 'english_words'
cachedir = Path(f'./cache/{wordlist_flavor}')
game, first_guess, second_guesses = load_state(wordlist_flavor, cachedir)

while True:
    if len(game.solution_space) == 1:
        print(f'Solution: {game.solution_space[0]}')
        break

    suggest = game.suggest()
    print(f'Suggested guess: {suggest}')
    guess, score = input('Enter guess and score: ').split()
    game.guess(guess, score)
    print()
