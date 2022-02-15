from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from flask import g
from server import db
from server.api.utils import token_required
from server.model import Todos

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')
post_parser.add_argument('duedate', type=str, required=True, location='form')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('todo_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('todo_id', type=int, required=True, location='args')

class TodoDone(Resource):
        
    @swagger.doc({
        'tags' : ['todo'],
        'description' : '끝낸 to do list 조회하기',
        'parameters' : [
        ],
        'responses' : {
            '200' : {
                'description' : '조회 성공'
            },
            '400' : {
                'description' : '조회 실패'
            }
        }
    })    
    def get(self):
        """끝난 to do list 조회하기"""
        
        all_done = Todos.query.filter(Todos.is_completed == 1).all()
        
        done_list = [done.get_data_object() for done in all_done]
        
        return {
            'code' : 200,
            'message' : '끝난 to do list 조회 성공',
            'data' : {
                'dones' : done_list,
            }
        }