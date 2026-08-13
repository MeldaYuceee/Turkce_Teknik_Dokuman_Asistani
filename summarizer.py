from sklearn.feature_extraction.text import TfidfVectorizer

from text_processing import split_sentences, STOP_WORDS


def create_summary(text, sentence_count=3):
    sentences = split_sentences(text)

    if len(sentences) <= sentence_count:
        return " ".join(sentences)

    vectorizer = TfidfVectorizer(
        stop_words=list(STOP_WORDS),
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(sentences)

    scores = matrix.sum(axis=1).A1

    ranked = scores.argsort()[::-1][:sentence_count]

    # Seçilen cümleleri metindeki eski sırasına göre göster.
    ranked = sorted(ranked)

    return " ".join(
        sentences[index]
        for index in ranked
    )
