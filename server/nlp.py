from gensim.models import KeyedVectors
from sklearn.neighbors import KNeighborsClassifier
import re
import numpy as np


word_model = KeyedVectors.load_word2vec_format(
    "server/numberbatch-en-17.06.txt.gz", binary=False
)
# word_model = []


def clean(sent):
    return re.compile("[^a-zA-Z0-9_]").sub(" ", str(sent)).lower().strip()


def embed(word):
    if word in word_model:
        norm = np.linalg.norm(word_model[word])
        return word_model[word] / norm
    else:
        return np.zeros(300)


with open("server/appearance.txt", "r") as f:
    WEAK_WORDS = list(set([clean(line.strip()) for line in f.readlines()]))
    WEAK_VECS = [embed(w) for w in WEAK_WORDS]
with open("server/categories.txt", "r") as f:
    STRONG_WORDS = list(set([clean(line.strip()) for line in f.readlines()]))
    STRONG_VECS = [embed(w) for w in STRONG_WORDS]
with open("server/bad_words.txt", "r") as f:
    BAD_WORDS = list(set([clean(line.strip()) for line in f.readlines()]))
    BAD_VECS = [embed(w) for w in BAD_WORDS]

relevant_classifier = KNeighborsClassifier(n_neighbors=2)
relevant_classifier.fit(BAD_VECS + WEAK_VECS + STRONG_VECS,
                        [0] * len(BAD_VECS) + [1] * (len(WEAK_VECS) + len(STRONG_VECS)))
strong_classifier = KNeighborsClassifier(n_neighbors=2)
strong_classifier.fit(BAD_VECS + WEAK_VECS + STRONG_VECS,
                        [0] * (len(BAD_VECS) + len(WEAK_VECS)) + [1] * len(STRONG_VECS))


def is_relevant(word):
    return relevant_classifier.predict([embed(word)])[0]


def is_strong(word):
    return strong_classifier.predict([embed(word)])[0]



def parse_page(title, desc):
    text = clean(title+desc)
    weak_keywords = []
    strong_keywords = []
    for word in text.split(" "):
        if not word:
            continue
        if is_strong(word):
            strong_keywords.append(word)
        elif is_relevant(word):
            weak_keywords.append(word)
    strong_keywords = " ".join(strong_keywords)
    weak_keywords = ",".join(weak_keywords)

    if strong_keywords and weak_keywords:
        keywords = strong_keywords + "+({})".format(weak_keywords)
    elif strong_keywords:
        keywords = strong_keywords
    elif weak_keywords:
        keywords = "({})".format(weak_keywords)
    else:
        keywords = []
    return title, keywords


def shorten_title(long_title):
    long_title = clean(long_title)
    weak_keywords = []
    strong_keywords = []
    for word in long_title.split(" "):
        if is_strong(word):
            strong_keywords.append(word)
        else:
            weak_keywords.append(word)
    strong_title = " ".join(strong_keywords).capitalize() + "."
    weak_title = " ".join(weak_keywords).capitalize() + "."
    return weak_title, strong_title


if __name__ == "__main__":
    print("Clean [this's so weird the 8heck: ", clean("this's so weird the 8heck"))
    print("Is strong [bernie]: ", is_strong("Bernie"))
    print("Is strong [red]: ", is_strong("Red"))
    print("Is strong [polo]: ", is_strong("Polo"))
    print("Weak title [Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red]: ", shorten_title("Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red")[0])
    print("Strong title [Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red]: ", shorten_title("Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red")[1])
    print("Extract [Skinny Stretch Jeans, Extra slim-fitting, cotton-denim jeans are made with some stretch for comfort in a classic five-pocket style.]: ", parse_page("Skinny Stretch Jeans", "Extra slim-fitting, cotton-denim jeans are made with some stretch for comfort in a classic five-pocket style."))