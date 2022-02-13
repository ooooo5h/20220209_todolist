from flask_restful import reqparse, Resource

class TodoDetail(Resource):
    
    def get(self, todo_id):
        return {
            '임시' : f"{todo_id}번 투두 상세보기"
        }