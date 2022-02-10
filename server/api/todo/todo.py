from flask_restful import Resource

class Todo(Resource):
    
    def get(self):
        return {
            '임시' : '임시 투두 겟'
        }