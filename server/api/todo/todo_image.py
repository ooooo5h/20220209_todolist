from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from werkzeug.datastructures import FileStorage

put_parser = reqparse.RequestParser()
put_parser.add_argument('image', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('todo_id', type=int, required=True, location='form')

class TodoImage(Resource):
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do 이미지 등록하기',
        'parameters' : [
            {
                'name' : 'todo_id',
                'description' : '사진을 첨부할 todo의 id',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True,
            },
            {
                'name' : 'image',
                'description' : '실제로 첨부할 이미지 파일',
                'in' : 'formData',
                'type' : 'file',
                'required' : True,
            }
        ],
        'responses' : {
            '200' : {
                'description' : '사진 첨부 성공'
            },
            '400' : {
                'description' : '사진 첨부 실패'
            },
        }
    })
    def put(self):
        """to do 이미지 등록하는 기능"""
        return {
            'code' : 'to do 이미지 등록하는 기능' 
        }