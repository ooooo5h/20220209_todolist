from flask_restful import Resource
from flask_restful_swagger_2 import swagger

class Todo(Resource):
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do list 생성하기',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : 'to do list 생성 성공' 
            },
            '400' : {
                'description' : 'to do list 생성 실패' 
            },    
        }
    })
    def get(self):
        """to do list를 생성합니다."""
        return {
            '임시' : '임시 투두 겟'
        }