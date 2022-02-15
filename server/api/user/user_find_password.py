from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server.model import Users
from server import db

import string, random

get_parser = reqparse.RequestParser()
get_parser.add_argument('u_id', type=str, required=True, location='args')
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')

class UserFindPassword(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 임시 비밀번호 찾기 ',
        'parameters' : [
            {
                'name' : 'u_id',
                'description' : '사용자 id',
                'in' : 'query',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'name',
                'description' : '사용자 이름',
                'in' : 'query',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'phone',
                'description' : '사용자 연락처',
                'in' : 'query',
                'type' : 'string',
                'required' : True,
            },
        ],
        'responses' : {
            '200' : {
                'description' : '임시 비밀번호 찾기 성공'
            },
            '400' : {
                'description' : '임시 비밀번호 찾기 실패'
            },
        }
    })
    def get(self):
        """비밀번호 찾기 : 임시 비밀번호 발급"""
        
        args = get_parser.parse_args()
        
        exist_u_id = Users.query.filter(Users.u_id == args['u_id']).first()
        
        if not exist_u_id:
            return {
                'code' : 400,
                'message' : '존재하지않는 사용자의 정보입니다. ID를 확인해주세요'
            }, 400
        
        # id가 일치하면, 이름 검사
        # 들어온 이름 vs id가 일치하는 유저의 이름                
        if args['name']  != exist_u_id.name:
            return {
                'code' : 400,
                'message' : '존재하지않는 사용자의 정보입니다. 이름을 확인해주세요'
            }, 400
        
        # id, 이름 일치하면 연락처 검사
        if args['phone'].replace('-', '') != exist_u_id.phone.replace('-',''):
            return {
                'code' : 400,
                'message' : '존재하지않는 사용자의 정보입니다. 연락처를 확인해주세요'
            }, 400
         
        # id, 이름, 연락처 모두 일치하는 유저를 찾았으면 임시비밀번호를 생성하여 알려주자
        # 생성할 비밀번호의 길이
        new_pw_len = 10
        # 영어 대소문자 = string.ascii_letters / 숫자 = string.digits / 특수문자 = string.punctuation
        pw_candidate = string.ascii_letters + string.digits
        
        new_pw = ''
        for i in range(new_pw_len):
            new_pw += random.choice(pw_candidate)
            
        # print('임시비밀번호', new_pw)
        
        # DB에 저장된 사용자의 비밀번호도 변경한 다음에 임시 비밀번호를 내려주기
        user = Users.query\
            .filter(Users.u_id == args['u_id'])\
            .filter(Users.name == args['name'])\
            .filter(Users.phone == args['phone'])\
            .first()
            
        user.u_pw = new_pw
        db.session.commit()
        
        return {
            'code' : 200,
            'message' : '비밀번호 조회 성공',
            'data' : {
                'u_pw' : f"임시 비밀번호는 '{new_pw}'입니다."
            }
        }
   