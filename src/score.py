from collections import Counter


def score_pair(guess: str, answer: str) -> list[int]:
    if len(answer) != len(guess):
        raise ValueError("Answer and guess must have the same length")

    score = [0] * len(answer)

    counter = Counter(list(answer))

    for idx, (a, g) in enumerate(zip(answer, guess)):
        if a == g:
            score[idx] = 2
            counter[a] -= 1

    for idx, g in enumerate(guess):
        if score[idx] == 0 and counter[g] > 0:
            score[idx] = 1
            counter[g] -= 1

    return score
