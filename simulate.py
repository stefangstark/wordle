from itertools import groupby
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from src.score import score_pair


def compute_score(guess, answer):
    return "".join(map(str, score_pair(guess=guess, answer=answer)))


def sort_by_entropy(gb, slnset):
    order = (
        gb["score"]
        .value_counts()
        .groupby("guess")
        .mean()
        .rename("mean_size")
        .reset_index()
    )
    order["in_slnset"] = order["guess"].isin(slnset)
    return order.sort_values(["mean_size", "in_slnset"], ascending=[True, False])


def play_round(answer, slnset, items):
    answer = str.encode(answer)
    next = None
    nguesses = 1

    while next != answer:
        gb = items.groupby("guess")
        next = sort_by_entropy(gb, slnset)["guess"].iloc[0]
        score = str.encode(compute_score(guess=next, answer=answer))
        group = gb.get_group(next)
        slnset = set(group.loc[group["score"] == score, "answer"])

        assert len(slnset) > 0
        assert answer in slnset
        assert nguesses < 10

        items = items.loc[items["answer"].isin(slnset)]

        nguesses = nguesses + 1

    return nguesses


def iterate_all_answers():
    def iterate(first):
        for answer in Path("./data/answers.csv").read_text().splitlines():
            yield compute_score(guess=first, answer=answer), answer

    for score, answers in groupby(iterate(first), lambda x: x[0]):
        cache = Path(f"./data/first-play-{first}/score-{score}-vs-answers.csv")
        assert cache.exists()
        allitems = pd.read_csv(cache, dtype="|S5")
        slnset = set(allitems["answer"])

        for _, answer in answers:
            yield answer, slnset, allitems


if __name__ == "__main__":
    first = "slate"
    history = dict()
    with open("./data/answers.csv") as f:
        nanswers = sum(1 for _ in f)

    for answer, slnset, items in tqdm(iterate_all_answers(), total=nanswers):
        history[answer] = play_round(answer, slnset, items)

    pd.Series(history).to_csv(f"./data/first-play-{first}/history.csv")
