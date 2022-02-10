from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

def create_app(config_name):
    app = Flask(__name__)
    
    CORS(app)
    
    app.config.from_object(f'server.config.{config_name}')
    
    api = Api(app, api_spec_url='/api/spec', title='to_do_list', api_version='0.1', catch_all_404s=True)
    
    
    from server.api.user import User
    from server.api.todo import Todo
    
    api.add_resource(User, '/user')
    api.add_resource(Todo, '/todo')
    
    
    
    return app