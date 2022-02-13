from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from server.model import Todos

class TodoDetail(Resource):

    @swagger.doc({
        'tags' : ['todo'],
        'description' : '특정 to do 상세보기',
        'parameters' : [
            {
                'name' : 'todo_id',
                'description' : '조회할 to do의 id 입력',
                'in' : 'path',
                'type' : 'integer',
                'required' : True,
            }
        ],
        'responses' : {
            '200' : {
                'description' : '조회 성공'
            },
            '400' : {
                'description' : '조회 실패'
            },
        }
    })
    def get(self, todo_id):
        """특정 to do 상세보기"""
        
        exist_todo_id = Todos.query.filter(Todos.id == todo_id).first()
        
        if not exist_todo_id :
            return {
                'code' : 400,
                'message' : f"{todo_id}번 to do는 존재하지 않습니다."
            }, 400
            
        return {
            'code' : 200, 
            'message' : f"{todo_id}번 to do 상세보기",
            'data' : {
                'todo' : exist_todo_id.get_data_object(need_user_info=True)
            }
        }