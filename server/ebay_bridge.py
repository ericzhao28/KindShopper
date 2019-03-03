'''
from ebaysdk.shopping import Connection as Shopping
shopping_api = Shopping(domain='svcs.ebay.com', version="671", appid=EBAY_APP_ID, config_file=None)
def shopping_api(parsed):
   response = shopping_api.execute('FindPopularItems', {'QueryKeywords': 'Python'})
   print(response.dict())
   print(response.reply)
'''

from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from .config import EBAY_APP_ID, EBAY_DEV_ID, EBAY_CERT_ID, \
    EBAY_TOKEN, SAND_EBAY_APP_ID, SAND_EBAY_DEV_ID, SAND_EBAY_CERT_ID, SAND_EBAY_TOKEN
import random
from pprint import pprint


finding_api = Finding(domain='svcs.ebay.com', appid=EBAY_APP_ID, config_file=None)
trading_api = Trading(domain='api.ebay.com', appid=EBAY_APP_ID, devid=EBAY_DEV_ID,
                      certid=EBAY_CERT_ID, token=EBAY_TOKEN, config_file=None)
# trading_api = Trading(domain='api.sandbox.ebay.com', appid=SAND_EBAY_APP_ID, devid=SAND_EBAY_DEV_ID,
#                      certid=SAND_EBAY_CERT_ID, token=SAND_EBAY_TOKEN, config_file=None)

cache = {}

def get_charity_name(charity_id):
    if charity_id in cache:
        return cache[charity_id]
    AVAILBLE_CHARITIES = ["Per Scholas, Inc.", "Feeding America", "The Humane Society of the United States", "United Way Worldwide", "World Central Kitchen, Inc", "Share Our Strength", "Action Against Hunger USA", "Heifer International", "Children's Hunger Fund", "Second Harvest Heartland", "The Nature Conservancy", "World Wildlife Fund", "Earthjustice", "Conservation International"]
    name = random.choice(AVAILBLE_CHARITIES)
    # trading_api.execute('GetCharities', {'CharityID': charity_id})
    # name = finding_api.response.reply.Charity.Name
    cache[charity_id] = name
    return name


def parse_search_results(items, item_cap=None):
    found = {}
    for item in items:
        if item["title"] not in found:
            found[item["title"]] = item
        else:
            if found[item["title"]]["sellingStatus"]["currentPrice"]["value"] > item["sellingStatus"]["currentPrice"]["value"]:
                found[item["title"]] = item

    found = list(found.values())
    if item_cap:
        found = found[:item_cap]

    for item in found:
        # pprint(dictstr['searchResult']['item'])
        print('Title: {}'.format(item['title']))
        print('URL: {}'.format(item['viewItemURL']))
        print("Image: {}".format(item["galleryURL"]))
        if "charityId" in item:
            print("Charity: {}".format(get_charity_name(item["charityId"])))
        if "material" in item:
            print("Material: {}".format(item["material"]))
        print('Price: {}'.format(item["sellingStatus"]["currentPrice"]["value"] + " "
                                 + item["sellingStatus"]["currentPrice"]["_currencyId"]))
    return found


def find_used(parsed):
    finding_api.execute("findItemsAdvanced", {
        'keywords': parsed,
        'itemFilter': [
            {'name': 'condition',
             'value': 'Used'},
        ],
        'paginationInput': {
            'entriesPerPage': '50',
            'pageNumber': '1'
        },
        'sortOrder': 'BestMatch'
    })

    dictstr = finding_api.response.dict()
    if "item" not in dictstr["searchResult"]:
        return []

    return parse_search_results(dictstr['searchResult']['item'], 5)


SUSTAINABLE_MATERIALS = ["organic cotton", "tencel", "lyocell", "hemp", "linen", "flax", "silk"]
def find_sustainable(parsed):
    all_items = []
    for material in SUSTAINABLE_MATERIALS:
        finding_api.execute("findItemsAdvanced", {
            'keywords': parsed + '"{}"'.format(material),
            'paginationInput': {
                'entriesPerPage': '50',
                'pageNumber': '1'
            },
            'sortOrder': 'BestMatch'
        })
        dictstr = finding_api.response.dict()
        if "item" in dictstr["searchResult"]:
            material_items = dictstr['searchResult']['item']
            for item in material_items:
                item["material"] = material
            all_items += material_items
    if not all_items:
        return []
    return parse_search_results(all_items, 5)


def find_charitable(parsed):
    finding_api.execute("findItemsAdvanced", {
        'keywords': parsed,
        'itemFilter': [
            {'name': 'CharityOnly',
             'value': 'True'},
        ],
        'paginationInput': {
            'entriesPerPage': '50',
            'pageNumber': '1'
        },
        'sortOrder': 'BestMatch'
    })
    dictstr = finding_api.response.dict()
    if "item" not in dictstr["searchResult"]:
        return []
    return parse_search_results(dictstr['searchResult']['item'], 5)


if __name__ == "__main__":
    find_sustainable(input("Keywords: "))
    find_charitable(input("Keywords: "))
    find_used(input("Keywords: "))