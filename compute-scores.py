from itertools import product
from pathlib import Path

from tqdm import tqdm

from src.score import score_pair

answers = Path("./data/answers.csv").read_text().splitlines()
valid_guesses = Path("./data/all.csv").read_text().splitlines()

outpath = Path("./data/scores-all-vs-answers.csv")
with open(outpath, "w") as f:
    for guess, answer in tqdm(list(product(valid_guesses, answers))):
        score = score_pair(guess=guess, answer=answer)
        f.write(f"{guess},{answer},{''.join(map(str, score))}\n")

outpath = Path("./data/scores-answers-vs-answers.csv")
with open(outpath, "w") as f:
    for guess, answer in tqdm(list(product(answers, answers))):
        score = score_pair(guess=guess, answer=answer)
        f.write(f"{guess},{answer},{''.join(map(str, score))}\n")
