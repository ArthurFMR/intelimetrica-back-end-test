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


@restaurants_bp.route('/restaurants', methods=['POST'])
def add_restaurant():
    if check_json_type(request):
        
        id = request.json['id']
        data = group_data_from_request(request.json)
        # Id is needed in the first position of the tuple
        data.insert(0, id)
      
        if restaurants.insert(tuple(data)):
            return jsonify(SUCCESSFUL_MSG), 201
        return jsonify(INTERNAL_ERROR), 500
    
    res = {'message': 'The type of the content must be json'}
    return jsonify(res), 400


@restaurants_bp.route('/restaurants', methods=['GET'])
def get_restaurants_list():
    data = restaurants.select_all()
    return jsonify(data), 200


@restaurants_bp.route('/restaurants', methods=['PUT'])
def edit_restaurant():
    if check_json_type(request):
        
        id = request.args.get('id')
        if id:
            data = group_data_from_request(request.json)
            # Id is needed in the last position of the tuple
            data.append(id)

            if restaurants.update(tuple(data)):
                return jsonify(SUCCESSFUL_MSG), 201
            return jsonify(INTERNAL_ERROR), 500
        
        response = {'message': 'URL must contains id argument value'}
        return jsonify(response), 400


@restaurants_bp.route('/restaurants', methods=['DELETE'])
def remove_restaurant():
    id = request.args.get('id')
    if id:
        if restaurants.delete(id):
            return jsonify(SUCCESSFUL_MSG), 200
        return jsonify(INTERNAL_ERROR), 500
    
    response = {'message': 'URL must contains id argument value'}
    return jsonify(response), 400


@restaurants_bp.route('/restaurants/statistics', methods=['GET'])
def find_restaurants():
    lng = request.args.get('longitude')
    lat = request.args.get('latitude')
    radius = request.args.get('radius')

    if lng and lat and radius:
        data = restaurants.find_restaurants_in_circle(lng, lat, radius)[0]
        return jsonify({'count': data[0], 'avg': float(data[1]), 'std': float(data[2])}), 200

    response = {'message': 'URL must contains all arguments value required'}
    return jsonify(response), 400


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

    # Asigning data to variables
    rating, name = json['rating'], json['name'] 
    site, email, phone = json['site'], json['email'], json['phone']
    street, city, state = json['street'], json['city'], json['state']
    lat, lng = json['lat'], json['lng']
    

    data = [rating, name, site, email, phone, street, city,
            state, lat, lng]
    
    return data
