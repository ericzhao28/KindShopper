from ebaysdk.finding import Connection
from config import EBAY_APP_ID

api = Connection(domain='svcs.sandbox.ebay.com', appid=EBAY_APP_ID, config_file=None)

api.execute('findItemsAdvanced', {
    'keywords': 'laptop',
    'categoryId': ['177', '111422'],
    'itemFilter': [
        {'name': 'Condition', 'value': 'Used'},
        {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'GBP'},
        {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'GBP'}
    ],
    'paginationInput': {
        'entriesPerPage': '25',
        'pageNumber': '1'
    },
    'sortOrder': 'CurrentPriceHighest'
})

dictstr = api.response.dict()

for item in dictstr['searchResult']['item']:
    print('ItemID: {}'.format(item['itemId']))
    print('Title: {}'.format(item['title']))
    print('CategoryID: {}'.format(item['primaryCategory']['categoryId']))
