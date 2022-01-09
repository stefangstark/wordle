def load_words(kind='english_words'):
    if kind == 'english_words':
        from english_words import english_words_lower_alpha_set as words

    elif kind == 'nltk':
        from nltk.corpus import words
        words = words.words()
        words = filter(lambda x: x.islower() and x.isalpha(), words)

    else:
        raise ValueError

    words = sorted(set(filter(lambda x: len(x) == 5, words)))
    return words