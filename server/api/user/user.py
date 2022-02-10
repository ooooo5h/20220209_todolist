# 사용자 정보와 관련된 기능들을 모아두는 모듈
from flask_restful import Resource
from flask_restful_swagger_2 import swagger

class User(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 정보 조회 기능',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '사용자 정보 조회 성공'
            },
            '400' : {
                'description' : '사용자 정보 조회 실패'
            },
        }
    })
    def get(self):
        """사용자의 정보를 조회합니다."""
        return {
            'code' : 200,
            'message' : '임시-사용자정보조회'
        }
   
    @swagger.doc({
        'tags' : ['user'],
        'description' : '로그인 기능',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '로그인 성공'
            },
            '400' : {
                'description' : '로그인 실패'
            },
        }
    })     
    def post(self):
        """로그인을 시도합니다."""
        return {
            'code' : 200,
            'message' : '임시-로그인기능'
        }

    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원가입 기능',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '회원가입 성공'
            },
            '400' : {
                'description' : '회원가입 실패'
            },
        }
    })
    def put(self):
        """회원가입을 합니다."""
        return {
            'code' : 200,
            'message' : '임시-회원가입기능'
        }