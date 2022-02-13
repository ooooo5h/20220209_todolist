from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

put_parser = reqparse.RequestParser()
put_parser.add_argument('image', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('todo_id', type=int, required=True, location='form')

class TodoImage(Resource):
    
    def put(self):
        return {
            'code' : 'to do 이미지 등록하는 기능' 
        }