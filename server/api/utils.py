# 토큰을 발급 + 토큰이 들어오면 그 사용자가 누구인지 분석하는 기능을 담당하는 파일.(JWT : Json Web Token )

from flask import current_app
import jwt
from server.model import Users
from functools import wraps
from flask_restful import reqparse

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, required=True, location='headers')

def encode_token(user):
    
    # 사용자의 어떤 항목으로 토큰을 만들지 => 복호화해서 꺼낼 것도 고려해야하기때문에 딕셔너리로 생성
    # 어떤 비밀키를 섞어서 암호화할지
    # 어떤 알고리즘으로 암호화할건지
    
    return jwt.encode(
        {'id' : user.id, 'u_id' : user.u_id, 'u_pw' : user.u_pw}, 
        current_app.config['JWT_SECRET'],
        algorithm = current_app.config['JWT_ALGORITHM'],
        )  # 실행 결과가 바로 토큰 str로 나오기 때문에 decode 필요없음
    
def decode_token(token):
        
    try:
        # 어떤 토큰을 해체할건지
        # 어떤 비밀키로 복호화할건지
        # 어떤 알고리즘으로 할건지
        decoded_dict = jwt.decode(
            token,
            current_app['JWT_SECRET'],
            algorithm = current_app.config['JWT_ALGORITHM'],   
        )
        
        user = Users.query\
            .filter(Users.id == decoded_dict['id'])\
            .filter(Users.u_id == decoded_dict['u_id'])\
            .filter(Users.u_pw == decoded_dict['u_pw'])\
            .first()
        return user
    
    except jwt.exceptions.DecodeError:
        # 잘못된 토큰이 들어와서 복호화에 실패했다면, 예외처리에 의해 이쪽 코드로 빠짐
        # 사용자 없다고 리턴해주기
        return None
    
# 데코레이터를 사용하자 => 추가 함수에 적힌 코드를 먼저 실행하고, 그 뒤에 실제함수를 진행시킴
def token_required(func):
    
    @wraps(func)
    def decorator(*args, **kwargs):
        # 1. 토큰 파라미터를 받고
        args = token_parser.parse_args()
        
        # 2. 그 토큰으로 실제 사용자를 검색
        user = decode_token(args['X-Http-Token'])
        
        # 3. 사용자가 있다면 실제함수 실행
        if user:
            return func(*args, **kwargs)
        
        # 4. 사용자가 없다면 403 에러 리턴
        else :
            return {
                'code' : 403,
                'message' : '올바르지 않은 토큰입니다.'
            }, 403
            
    return decorator