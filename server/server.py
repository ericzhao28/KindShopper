"""
Backend API logic.
"""

from flask import request, jsonify, Flask
from flask_cors import CORS

from .find import find_products


# FlaskAPI does not support flask_graphql, using Flask instead
app = Flask(__name__)
cors = CORS(app)

# Main endpoint
@app.route("/get_alts", methods=['POST'])
def get_alts_route():
    """ Upload a new message. """
    try:
        title = request.json["title"]
        desc = request.json["desc"]
        search_query = request.json["query"]
        print("Title: ", title)
        print("Desc: ", desc)
        print("Search: ", search_query)
        products = find_products(title, desc, search_query)
        print(products)
        return jsonify({"success": True, "products": products})
    except AssertionError:
        return jsonify({"success": False})

# Main endpoint
@app.route("/get_alts_temp", methods=['POST'])
def get_alts_route_temp():
    """ Upload a new message. """
    try:
        title = request.json["title"]
        desc = request.json["desc"]
        products = [{"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
     "title": "Patagonia SS Men's",
     "deal_type": "ecofriendly",
     "desc": "Patagonia SS Men's Size",
     "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
     "price": "$43"},
    {"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
     "title": "Patagonia SS Men's",
     "deal_type": "charitable",
     "desc": "Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red",
     "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
     "price": "$43"},
    {"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
     "title": "Patagonia SS Men's",
     "deal_type": "reused",
     "desc": "Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red",
     "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
     "price": "$43"}]
        return jsonify({"success": True, "products": products})
    except AssertionError:
        return jsonify({"success": False})
