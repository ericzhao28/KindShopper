"""
Backend API logic.
"""

from flask import request, jsonify, Flask
from flask_cors import CORS

from nlp import parse_page
from ebay_bridge import find_products


# FlaskAPI does not support flask_graphql, using Flask instead
app = Flask(__name__)
cors = CORS(app)

# Main endpoint
@app.route("/get_alts", methods=['POST'])
def get_alts_route():
    """ Upload a new message. """
    try:
        parsed = parse_page(str(request.json["product_description"]))
        print(parsed)
        products = find_products(parsed)
        print(products)
        return jsonify({"success": True, "products": products})
    except AssertionError:
        return jsonify({"success": False})