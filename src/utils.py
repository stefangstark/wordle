import csv
import itertools
from collections import Counter, namedtuple

from scipy.stats import entropy

Guess = namedtuple("Guess", "guess answer score")


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
