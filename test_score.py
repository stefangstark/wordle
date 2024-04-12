from src.score import score_pair


def score(*args, **kwargs):
    return "".join(map(str, score_pair(*args, **kwargs)))


def test_score():
    assert score("never", "never") == "22222"
    assert score("lever", "never") == "02222"
    assert score("never", "about") == "00000"
    assert score("lever", "queen") == "01020"
    assert score("abcee", "queen") == "00021"
    assert score("abcde", "eabcd") == "11111"
    assert score("xxxxx", "xxxxy") == "22220"
    assert score("slate", "bigot") == "00010"
