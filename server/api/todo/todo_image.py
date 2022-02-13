from flask_restful import Resource

class TodoImage(Resource):
    
    def put(self):
        return {
            'code' : 'to do 이미지 등록하는 기능' 
        }