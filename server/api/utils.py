# 토큰을 발급 + 토큰이 들어오면 그 사용자가 누구인지 분석하는 기능을 담당하는 파일.(JWT : Json Web Token )

from flask import current_app
import jwt

def encode_token(user):
    
    # 사용자의 어떤 항목으로 토큰을 만들지 => 복호화해서 꺼낼 것도 고려해야하기때문에 딕셔너리로 생성
    # 어떤 비밀키를 섞어서 암호화할지
    # 어떤 알고리즘으로 암호화할건지
    
    return jwt.encode(
        {'id' : user.id, 'u_id' : user.u_id, 'u_pw' : user.pw}, 
        current_app.config['JWT_SECRET'],
        algorithm = current_app.config['JWT_ALGORITHM'],
        ).decode('utf-8')