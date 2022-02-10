# 사용자 정보와 관련된 기능들을 모아두는 모듈
from flask_restful import Resource

class User(Resource):
    
    def get(self):
        return {
            'code' : 200,
            'message' : '임시-사용자정보조회'
        }
        
    def post(self):
        return {
            'code' : 200,
            'message' : '임시-로그인기능'
        }

    def put(self):
        return {
            'code' : 200,
            'message' : '임시-회원가입기능'
        }