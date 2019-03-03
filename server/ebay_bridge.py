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
    AVAILBLE_CHARITIES = ["Per Scholas, Inc.", "Feeding America", "The Humane Society", "United Way Worldwide", "World Central Kitchen", "Share Our Strength", "Action Against Hunger USA", "Heifer International", "Children's Hunger Fund", "Second Harvest Heartland", "The Nature Conservancy", "World Wildlife Fund", "Earthjustice", "Conservation International"]
    name = random.choice(AVAILBLE_CHARITIES)
    # trading_api.execute('GetCharities', {'CharityID': charity_id})
    # name = finding_api.response.reply.Charity.Name
    cache[charity_id] = name
    return name


def parse_search_results(items, shorten_title, item_cap=None):
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

    revised = []
    for item in found:
        price = "$" + item["sellingStatus"]["currentPrice"]["value"]
        num_price = float(item["sellingStatus"]["currentPrice"]["value"])
        image_url = item["galleryURL"]
        deal_url = item["viewItemURL"]
        desc, title = shorten_title(item["title"])
        if "charityId" in item:
            desc += " Proceeds towards {}.".format(get_charity_name(item["charityId"]))
            deal_type = "charitable"
        elif "material" in item:
            desc += " Made w/ eco-friendly {}.".format(item["material"])
            deal_type = "ecofriendly"
        else:
            desc += " Prevent waste and save: buy used!"
            deal_type = "reused"
        revised.append(
            {
                "price": price,
                "num_price": num_price,
                "image_url": image_url,
                "deal_url": deal_url,
                "title": title,
                "deal_type": deal_type,
                "desc": desc
            }
        )
    return revised


def find_used(parsed):
    finding_api.execute("findItemsAdvanced", {
        'keywords': parsed,
        'itemFilter': [
            {'name': 'condition',
             'value': 'Used'},
        ],
        'paginationInput': {
            'entriesPerPage': '10',
            'pageNumber': '1'
        },
        'sortOrder': 'BestMatch'
    })

    dictstr = finding_api.response.dict()
    if "item" not in dictstr["searchResult"]:
        return []
    return dictstr['searchResult']['item']


SUSTAINABLE_MATERIALS = ["organic cotton", "tencel", "lyocell", "hemp", "linen", "flax", "silk"]
def find_sustainable(parsed):
    all_items = []
    for material in SUSTAINABLE_MATERIALS:
        finding_api.execute("findItemsAdvanced", {
            'keywords': parsed + '"{}"'.format(material),
            'paginationInput': {
                'entriesPerPage': '10',
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
    return all_items


def find_charitable(parsed):
    finding_api.execute("findItemsAdvanced", {
        'keywords': parsed,
        'itemFilter': [
            {'name': 'CharityOnly',
             'value': 'True'},
        ],
        'paginationInput': {
            'entriesPerPage': '10',
            'pageNumber': '1'
        },
        'sortOrder': 'BestMatch'
    })
    dictstr = finding_api.response.dict()
    if "item" not in dictstr["searchResult"]:
        return []
    return dictstr['searchResult']['item']


if __name__ == "__main__":
    get_charity_name("21220")
    print(find_sustainable(input("Keywords: ")))
    print(find_charitable(input("Keywords: ")))
    print(find_used(input("Keywords: ")))