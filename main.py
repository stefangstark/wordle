import csv
import itertools
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from scipy.stats import entropy


@dataclass
class Guess:
    guess: str
    answer: str
    score: str


def groupby(iterable, key, presorted=False):
    if not presorted:
        iterable = sorted(iterable, key=key)

    return itertools.groupby(iterable, key=key)


def load(path):
    with open(path) as f:
        reader = csv.reader(f)
        for guess, answer, score in reader:
            yield Guess(guess, answer, score)


def compute_entropy(groups, include=None):
    ent = dict()
    for k, items in groups.items():
        counter = Counter(
            x.score for x in items if include is None or x.answer in include
        )
        ent[k] = entropy(list(counter.values()), base=2)
    return ent


cache = Path("./data/scores-answers-vs-answers.csv")
items = list(load(cache))
groups = {k: list(g) for k, g in groupby(items, lambda x: x.guess)}


# first = compute_entropy(groups)
key = "slate"
df = list()

for score, items in groupby(groups[key], lambda x: x.score):
    slnset = set(item.answer for item in items)
    ent = compute_entropy(groups, include=slnset)
    top = sorted(ent.items(), key=lambda x: (x[1], x[0] in slnset), reverse=True)
    best = top[0][1]
    if best == 0:
        continue

    for idx, (second, e) in enumerate(top):
        df.append((score, len(slnset), idx, second, e, e / best))

pd.DataFrame(
    df, columns=["score", "nwords", "idx", "guess", "entropy", "normalized_entropy"]
).to_csv("foo.csv.gz")
