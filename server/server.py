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
        page_info = request.json["page_info"]
        print(page_info)
        products = find_products(page_info)
        print(products)
        return jsonify({"success": True, "products": products})
    except AssertionError:
        return jsonify({"success": False})