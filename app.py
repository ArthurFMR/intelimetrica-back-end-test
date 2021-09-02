from flask import Flask
from flask_cors import CORS

from resources.restaurants import restaurants_bp

app = Flask(__name__)
cors = CORS(app, resources={r"/api/": {"origins": "*"}})

app.register_blueprint(restaurants_bp)


if __name__ == '__main__':
    app.run(debug=True)