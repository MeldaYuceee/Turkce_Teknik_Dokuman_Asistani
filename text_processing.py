import re


STOP_WORDS = {
    "acaba", "ama", "ancak", "artık", "aslında", "az",
    "bazı", "belki", "bile", "bir", "birçok", "birkaç",
    "biz", "bu", "bunun", "da", "daha", "de", "defa",
    "diye", "en", "gibi", "hem", "henüz", "her", "hiç",
    "için", "ile", "ise", "kadar", "ki", "kim", "mı",
    "mi", "mu", "mü", "nasıl", "ne", "neden", "nerede",
    "nereye", "niçin", "o", "olan", "olarak", "onun",
    "sadece", "şey", "şu", "tüm", "ve", "veya", "ya",
    "yani", "çok", "sonra", "önce"
}


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def normalize_word(word):
    word = word.lower().strip(".,!?;:%()[]{}\"'")

    # Çok sık kullanılan Türkçe ekleri tamamen bir dilbilimsel
    # kök bulma işlemi yapmadan sadeleştirir.
    suffixes = [
        "lerinin", "larının", "lerden", "lardan",
        "lerinin", "larının", "ların", "lerin",
        "ların", "lerin", "dan", "den",
        "dır", "dir", "dur", "dür",
        "tır", "tir", "tur", "tür",
        "ına", "ine", "una", "üne",
        "ını", "ini", "unu", "ünü",
        "ının", "inin", "unun", "ünün",
        "ları", "leri",
        "lar", "ler",
        "dan", "den",
        "da", "de",
        "ta", "te",
        "ı", "i", "u", "ü"
    ]

    for suffix in suffixes:
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            word = word[:-len(suffix)]
            break

    return word


def is_useful_word(word):
    word = normalize_word(word)

    if len(word) < 4:
        return False

    if word in STOP_WORDS:
        return False

    return True
