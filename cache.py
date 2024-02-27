import csv
import sys
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from src.utils import load

_, first = sys.argv

cache = Path("./data/scores-all-vs-answers.csv")

index_score_to_answer = defaultdict(list)
index_answer_to_items = defaultdict(list)

for item in load(cache):
    index_answer_to_items[item.answer].append(item)
    if item.guess == first:
        index_score_to_answer[item.score].append(item.answer)

outdir = Path(f"./data/first-play-{first}")
outdir.mkdir(exist_ok=True, parents=True)

it = tqdm(index_score_to_answer.items(), total=len(index_score_to_answer))
for score, answers in it:
    outpath = outdir / f"score-{score}-vs-answers.csv"
    # with gzip.open(outpath, "w") as f:
    with open(outpath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["guess", "answer", "score"])

        for answer in answers:
            for item in index_answer_to_items[answer]:
                writer.writerow([item.guess, item.answer, item.score])
