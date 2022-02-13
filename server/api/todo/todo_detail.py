from flask_restful import Resource
from server.model import Todos

class TodoDetail(Resource):
    
    def get(self, todo_id):
        
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