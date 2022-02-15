from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server.model import Users

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')

class UserFindId(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 ID 찾기 ',
        'parameters' : [
            {
                'name' : 'name',
                'description' : '이름',
                'in' : 'query',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'phone',
                'description' : '연락처',
                'in' : 'query',
                'type' : 'string',
                'required' : True,
            },
        ],
        'responses' : {
            '200' : {
                'description' : '아이디 찾기 성공'
            },
            '400' : {
                'description' : '아이디 찾기 실패'
            },
        }
    })
    def get(self):
        """사용자의 아이디를 찾습니다."""
        
        args = get_parser.parse_args()
        
        exist_user = Users.query.filter(Users.name == args['name']).filter(Users.phone == args['phone']).first()
        
        if not exist_user:
            return {
                'code' : 400,
                'message' : '존재하지않는 사용자의 정보입니다.'
            }, 400
        
        return {
            'code' : 200,
            'message' : 'id조회 성공',
            'data' : {
                'user_id' : exist_user.u_id,
            }
        }
   