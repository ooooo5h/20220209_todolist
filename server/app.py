from flask import Flask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    
    CORS(app)
    
    app.config.from_object(f'server.config.{config_name}')
    
    return app