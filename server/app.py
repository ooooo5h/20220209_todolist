from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint

# DB와 연동 하기
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    CORS(app)
    
    app.config.from_object(f'server.config.{config_name}')
    
    db.init_app(app)
    
    api = Api(app, api_spec_url='/api/spec', title='to_do_list', api_version='0.1', catch_all_404s=True)
    
    
    from server.api.user import User, UserFindId, UserFindPassword
    from server.api.todo import Todo, TodoDetail, TodoImage, TodoDone, TodoByDueDate
    
    api.add_resource(User, '/user')
    api.add_resource(UserFindId, '/user/findid')
    api.add_resource(UserFindPassword, '/user/findpw')
    api.add_resource(Todo, '/todo')
    api.add_resource(TodoByDueDate, '/todo/orderbyduedate')
    api.add_resource(TodoDone, '/todo/done')
    api.add_resource(TodoDetail, '/todo/<int:todo_id>')
    api.add_resource(TodoImage, '/todoimage')
    
    
    # swagger문서를 자동으로 생성하기
    swagger_ui = get_swaggerui_blueprint('/api/docs', '/api/spec.json', config={'app_name' : 'TO_DO_LIST'})
    
    # Flask앱의 url에 swagger문서를 등록하기
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')
    
    return app