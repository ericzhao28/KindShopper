from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
# from ebaysdk.shopping import Connection as Shopping
from config import EBAY_APP_ID, EBAY_DEV_ID, EBAY_CERT_ID, EBAY_TOKEN
from pprint import pprint


finding_api = Finding(domain='svcs.ebay.com', appid=EBAY_APP_ID, config_file=None)
# shopping_api = Shopping(domain='svcs.ebay.com', version="671", appid=EBAY_APP_ID, config_file=None)
trading_api = Trading(domain='api.ebay.com', appid=EBAY_APP_ID, devid=EBAY_DEV_ID,
                      certid=EBAY_CERT_ID, token=EBAY_TOKEN, config_file=None)

# def shopping_api(parsed):
#    response = shopping_api.execute('FindPopularItems', {'QueryKeywords': 'Python'})
#    print(response.dict())
#    print(response.reply)

cache = {}

def get_charity_name(charity_id):
    if charity_id in cache:
        return cache[charity_id]

    response = trading_api.execute('GetUser', {})
    print(response.dict())

    trading_api.execute('GetCharities', {'CharityID': charity_id})

    name = finding_api.response.reply.Charity.Name
    cache[charity_id] = name
    return name


def find_products(parsed):
    finding_api.execute("findItemsAdvanced", {
        'keywords': 'red t-shirt',
        'itemFilter': [
            {'name': 'CharityOnly',
             'value': 'True'},
        ],
        'paginationInput': {
            'entriesPerPage': '5',
            'pageNumber': '1'
        },
        'sortOrder': 'BestMatch'
    })

    dictstr = finding_api.response.dict()
    if "item" not in dictstr["searchResult"]:
        return []

    for item in dictstr['searchResult']['item']:
        pprint(dictstr['searchResult']['item'])
        print('Title: {}'.format(item['title']))
        print('URL: {}'.format(item['viewItemURL']))
        if "charityId" in item:
            print(item["charityId"])
            print(get_charity_name(item["charityId"]))
        print('Price: {}'.format(item["sellingStatus"]["currentPrice"]["value"] + " "
                                 + item["sellingStatus"]["currentPrice"]["_currencyId"]))

    products = [x for x in dictstr['searchResult']['item']]
    return products


find_products(None)
# find_charitable(None)