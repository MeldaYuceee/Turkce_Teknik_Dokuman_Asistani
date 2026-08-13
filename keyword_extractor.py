import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer

from text_processing import (
    STOP_WORDS,
    is_useful_word,
    normalize_word
)


EXTRA_WORDS = {
    "şekilde", "sürekli", "durum", "durumda",
    "özellikle", "birlikte", "tarafından",
    "sayede", "sonucunda", "aracın", "araca",
    "aracı", "süresini", "süresi", "sistem",
    "sistemi"
}


def get_words(text):
    words = re.findall(
        r"[A-Za-zÇĞİÖŞÜçğıöşü0-9]+",
        text.lower()
    )

    result = []

    for word in words:
        normalized = normalize_word(word)

        if not is_useful_word(word):
            continue

        if normalized in EXTRA_WORDS:
            continue

        result.append(normalized)

    return result


def find_keywords(text, count=8):
    words = get_words(text)

    if not words:
        return []

    word_text = " ".join(words)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1
    )

    matrix = vectorizer.fit_transform([word_text])

    names = vectorizer.get_feature_names_out()
    scores = matrix.toarray()[0]

    frequency = Counter(words)

    candidates = []

    for index, name in enumerate(names):
        score = scores[index]

        if score <= 0:
            continue

        parts = name.split()

        if any(part in STOP_WORDS for part in parts):
            continue

        # İki kelimelik teknik ifadeleri biraz öne çıkar.
        phrase_bonus = 1.15 if len(parts) == 2 else 1.0

        frequency_bonus = min(
            1.20,
            1 + (frequency[name] * 0.03)
        )

        final_score = (
            score *
            phrase_bonus *
            frequency_bonus
        )

        candidates.append(
            (name, final_score)
        )

    candidates.sort(
        key=lambda item: item[1],
        reverse=True
    )

    keywords = []

    for word, _ in candidates:
        if word in keywords:
            continue

        # Aynı kelimenin hem tekli hem ikili halini
        # arka arkaya göstermemeye çalış.
        if len(word.split()) == 1:
            if any(word in item.split() for item in keywords):
                continue

        keywords.append(word)

        if len(keywords) >= count:
            break

    return keywords
