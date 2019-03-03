from .nlp import parse_page, shorten_title
from .ebay_bridge import find_used, find_sustainable, find_charitable, parse_search_results
import random


def autobalance(used, sustainable, charitable):
    lengths = sorted([len(used), len(sustainable), len(charitable)])
    if min(lengths) < 5:
        length = max(lengths)
    else:
        length = int(float(lengths[0] + lengths[1]) / 2.0)
    used = used[:length]
    sustainable = sustainable[:length]
    charitable = charitable[:length]
    results = used+sustainable+charitable
    random.shuffle(results)
    return results


def find_products(title, desc, search_query):
    exact, soft = parse_page(title, desc, search_query)
    print("Exact: ", exact)
    print("Soft: ", soft)
    used = parse_search_results(find_used(exact), shorten_title)
    sustainable = parse_search_results(find_sustainable(soft), shorten_title)
    charitable = parse_search_results(find_charitable(soft), shorten_title)
    print(len(used), len(sustainable), len(charitable))
    return autobalance(used, sustainable, charitable)


if __name__ == "__main__":
    print(find_products("Skinny Stretch Jeans", "Extra slim-fitting, cotton-denim jeans are made with some stretch for comfort in a classic five-pocket style."))