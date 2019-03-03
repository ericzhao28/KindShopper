from .nlp import parse_page
from .ebay_bridge import find_used, find_sustainable, find_charitable


def find_products(product_page):
    exact, soft = parse_page(product_page)
    used = find_used(exact)
    sustainable = find_sustainable(soft)
    charitable = find_charitable(soft)
