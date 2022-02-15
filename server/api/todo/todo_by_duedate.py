from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from server.model import Todos        
        
class TodoByDueDate(Resource):
    @swagger.doc({
        'tags' : ['todo'],
        'description' : '모든 to do list 조회하기(마감일 순)',
        'parameters' : [
        ],
        'responses' : {
            '200' : {
                'description' : '마감일 순 조회 성공'
            },
            '400' : {
                'description' : '조회 실패'
            }
        }
    })    
    def get(self):
        """모든 to do list 조회하기(마감일 순)"""
        
        all_to_do = Todos.query.order_by(Todos.duedate).all()
        
        to_do_list = [todo.get_data_object() for todo in all_to_do]
        
        return {
            'code' : 200,
            'message' : '마감일 순으로 to do list 조회 성공',
            'data' : {
                'todos' : to_do_list,
            }
        }