from flask import json, request, jsonify, Blueprint

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


@restaurants_bp.route('/restaurants', methods=['POST'])
def add_restaurant():
    if check_json_type(request):
        data = group_data_from_request(request.json)

        if restaurants.insert(data):
            return jsonify(SUCCESSFUL_MSG), 201
        return jsonify(INTERNAL_ERROR), 500
    
    res = {'message': 'The type of the content must be json'}
    return jsonify(res), 400


def check_json_type(req):
    """Check if Content-Type is Json"""

    if req.headers['Content-Type'] == 'application/json':
        return True
    return False


def group_data_from_request(json):
    """As the amount of data of Add and Update actions are too many,
    this function is going to group the common data into a
    tuple
    """

    id = json['id']
    rating = json['rating']
    name = json['name']
    site = json['site']
    email = json['email']
    phone = json['phone']
    street = json['street']
    city = json['city']
    state = json['state']
    lat = json['lat']
    lng = json['lng']

    data = (id, rating, name, site, email, phone, street, city,
            state, lat, lng)
    
    return data
