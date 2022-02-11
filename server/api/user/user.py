# 사용자 정보와 관련된 기능들을 모아두는 모듈
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server.model import Users
from server import db

post_parser = reqparse.RequestParser()
post_parser.add_argument('u_id', type=str, required=True , location='form')
post_parser.add_argument('u_pw', type=str, required=True , location='form')

put_parser = reqparse.RequestParser()
put_parser.add_argument('u_id', type=str, required=True, location='form')
put_parser.add_argument('u_pw', type=str, required=True, location='form')
put_parser.add_argument('name', type=str, required=True, location='form')
put_parser.add_argument('nickname', type=str, required=True, location='form')

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
        
        login_user = Users.query.filter(Users.u_id == args['u_id']).filter(Users.u_pw == args['u_pw']).first()
          
        if login_user:            
            return {
                'code' : 200,
                'message' : '로그인 성공',
                'data' : {
                    'user' : login_user.get_data_object(),
                }
            }
        else : 
            return {
                'code' : 400,
                'message' : '로그인에 실패했습니다.'
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
            }
        
        # 조건 충족했으면 DB에 저장
        new_user = Users()
        new_user.u_id = args['u_id']
        new_user.u_pw = args['u_pw']
        new_user.name = args['name']
        new_user.nickname = args['nickname']
        
        db.session.add(new_user)
        db.session.commit()
               
        return {
            'code' : 200,
            'message' : f"{args['name']}님, 회원가입에 성공하셨습니다.",
        }