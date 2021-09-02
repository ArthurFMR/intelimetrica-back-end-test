from flask import request, jsonify, Blueprint

from models import restaurants

INTERNAL_ERROR = {'message': 'Internal Error in the server'}
SUCCESSFUL_MSG = {'message': 'successful'}

# Blueprint for separating routes from app.py
restaurants_bp = Blueprint('routes-resources-restaurants', __name__)


@restaurants_bp.route('/restaurants/load-csv-data', methods=['POST'])
def load_data():
    url = request.args.get('url')

    if url:
        # If this function run successfuly return 200 response
        if restaurants.load_csv_data(url):
            return jsonify(SUCCESSFUL_MSG), 200
        # Otherwise return 500 response if there is an error
        return jsonify(INTERNAL_ERROR), 500
    else:
        # Return 400 for bad request
        response = {'message': 'URL must contains url argument value'}
        return jsonify(response), 400