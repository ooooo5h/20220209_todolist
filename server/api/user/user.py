# 사용자 정보와 관련된 기능들을 모아두는 모듈
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from flask import g

from server.api.utils import encode_token, token_required
from server.model import Users
from server import db

import datetime

post_parser = reqparse.RequestParser()
post_parser.add_argument('u_id', type=str, required=True , location='form')
post_parser.add_argument('u_pw', type=str, required=True , location='form')

put_parser = reqparse.RequestParser()
put_parser.add_argument('u_id', type=str, required=True, location='form')
put_parser.add_argument('u_pw', type=str, required=True, location='form')
put_parser.add_argument('name', type=str, required=True, location='form')
put_parser.add_argument('nickname', type=str, required=True, location='form')
put_parser.add_argument('phone', type=str, required=True, location='form')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')

class User(Resource):
    
    # @swagger.doc({
    #     'tags' : ['user'],
    #     'description' : '사용자 정보 조회 기능',
    #     'parameters' : [
            
    #     ],
    #     'responses' : {
    #         '200' : {
    #             'description' : '사용자 정보 조회 성공'
    #         },
    #         '400' : {
    #             'description' : '사용자 정보 조회 실패'
    #         },
    #     }
    # })
    # def get(self):
    #     """사용자의 정보를 조회합니다."""
    #     return {
    #         'code' : 200,
    #         'message' : '임시-사용자정보조회'
    #     }
   
    @swagger.doc({
        'tags' : ['user'],
        'description' : '로그인 기능',
        'parameters' : [
            {
                'name' : 'u_id',
                'description' : '로그인할 아이디',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'u_pw',
                'description' : '로그인할 비밀번호',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            }
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
        
        args = post_parser.parse_args()
        
        # 입력한 id와 DB에 저장된 아이디가 같은 지 쿼리를 날려서 하나만 찾아와라
        login_user_id = Users.query.filter(Users.u_id == args['u_id']).first()
        
        if login_user_id is None :
            # 일치하는 ID가 없음
            return {
                'code' : 400,
                'message' : '아이디가 틀렸습니다.'
            }, 400
        
        if login_user_id.u_pw == args['u_pw'] :
            # 일차하는 ID가 있고, 그 유저 정보의 PW와 입력한 PW가 일치하는 경우
            return {
                'code' : 200,
                'message' : '로그인 성공',
                'data' : {
                    'user' : login_user_id.get_data_object(),
                    'token' : encode_token(login_user_id)
                }
            }
        else : 
            # 아이디는 맞지만, 비밀번호가 틀린 경우
            return {
                'code' : 400,
                'message' : '비밀번호가 틀렸습니다.'
            }, 400


    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원가입 기능',
        'parameters' : [
            {
                'name' : 'u_id',
                'description' : '사용할 아이디',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'u_pw',
                'description' : '사용할 비밀번호',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'name',
                'description' : '이름',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'nickname',
                'description' : '사용할 닉네임',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'phone',
                'description' : '사용할 연락처',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
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
        
        args = put_parser.parse_args()
        
        user_sign_in = Users.query
        
        # 중복된 아이디 사용 불가        
        exist_u_id = user_sign_in.filter(Users.u_id == args['u_id']).first()
        
        if exist_u_id:
            return {
                'code' : 400,
                'message' : f"{args['u_id']}은/는 이미 사용중인 아이디입니다."
            }, 400
        
        # 중복된 닉네임 사용 불가    
        exist_nickname = user_sign_in.filter(Users.nickname == args['nickname']).first()
        
        if exist_nickname:
            return {
                'code' : 400,
                'message' : f"{args['nickname']}은/는 이미 사용중인 닉네임입니다."
            }, 400
        
        # 조건 충족했으면 DB에 저장
        new_user = Users()
        new_user.u_id = args['u_id']
        new_user.u_pw = args['u_pw']
        new_user.name = args['name']
        new_user.nickname = args['nickname']
        new_user.phone = args['phone']
        
        db.session.add(new_user)
        db.session.commit()
               
        return {
            'code' : 200,
            'message' : f"{args['name']}님, 회원가입에 성공하셨습니다.",
            'data' : {
                'user' : new_user.get_data_object(),
                'token' : encode_token(new_user),
            }
        }
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원 탈퇴',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '사용자의 토큰값',
                'in' : 'header',
                'type' : 'string',
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '삭제 성공',
            },
            '400' : {
                'description' : '삭제 실패',
            }
        }
    })
    @token_required
    def delete(self):
        """회원 탈퇴"""
        
        # 실제 존재하는 회원 번호인가
        exist_user = g.user
        
        exist_user.u_id = '삭제'
        exist_user.u_pw = '삭제'
        exist_user.name = '삭제'
        exist_user.nickname = '삭제'
        exist_user.signout_at = datetime.datetime.utcnow()
        
        db.session.add(exist_user)
        db.session.commit()
        
        return {
            'code' : '200',
            'message' : '회원 삭제 성공',
        }
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원 정보 수정',
        'parameters' : [
            {
                'name' : 'id',
                'description' : '몇 번 사용자의 정보를 수정할건지?',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True,
            },
            {
                'name' : 'field',
                'description' : '변경하고 싶은 값',
                'in' : 'formData',
                'type' : 'string',
                'enum' : ['u_pw', 'nickname'],
                'required' : True,
            },
            {
                'name' : 'value',
                'description' : '변경하고 싶은 값',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
        ],
        'responses' : {
            '200' : {
                'description' : '회원 정보 수정 성공'
            },
            '400' : {
                'description' : '회원 정보 수정 실패'
            },
        }
    })    
    def patch(self):
        """회원 정보 수정"""
        
        args = patch_parser.parse_args()
        
        exist_user = Users.query.filter(Users.id == args['id']).first()
        
        if exist_user is None:
            return {
                'code' : 400,
                'message' : '존재하지 않는 사용자번호입니다.'
            }, 400
        
        if args['field'] == 'u_pw':
            exist_user.u_pw = args['value']
            
            db.session.add(exist_user)
            db.session.commit()
            
            return {
                'code' : 200,
                'message' : '비밀번호 변경 성공'
            }            
        
        elif args['field'] == 'nickname':
            exist_user.nickname = args['value']
            
            db.session.add(exist_user)
            db.session.commit()
    
            return {
                'code' : 200,
                'message' : '닉네임 변경 성공'
            }  
    
        return {
            'code' : 400,
            'message' : '회원정보 수정 실패'
        }, 400