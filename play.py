from pathlib import Path

import pandas as pd
from scipy.stats import entropy


def sort_by_entropy(gb, slnset):
    order = (
        gb["score"]
        .value_counts()
        .groupby("guess")
        .apply(lambda x: entropy(x, base=2.0))
        .rename("entropy")
        .reset_index()
    )
    order["in_slnset"] = order["guess"].isin(slnset)
    return order.sort_values(["entropy", "in_slnset"], ascending=[False, False])


guess = input("Enter guess [slate]: ") or "slate"
score = input("Enter score: ")

cache = Path(f"./data/first-play-{guess}/score-{score}-vs-answers.csv")
assert cache.exists()
items = pd.read_csv(cache, dtype="|S5")
slnset = set(items["answer"])

while True:
    print("\nPossible words: ", len(slnset))
    if len(slnset) < 20:
        print("  " + "\n  ".join(map(str, sorted(slnset))))

    gb = items.groupby("guess")
    order = sort_by_entropy(gb, slnset)
    print("\nSuggestions")
    for _, row in order.iloc[:5].iterrows():
        ent = entropy(
            gb.get_group(row["guess"])["score"].value_counts().values, base=2.0
        )
        print(f"  {row['guess'].decode()}: {ent:.2f}")
    print("\n")

    guess = str.encode(
        input(f"Enter guess [{order.iloc[0,0].decode()}]: ")
        or order.iloc[0, 0].decode()
    )
    score = str.encode(input("Enter score: "))
    if score == b"22222":
        print("Congrats!")
        break

    slnset = set(gb.get_group(guess).query("score == @score")["answer"])
    items = items.loc[items["answer"].isin(slnset)]
