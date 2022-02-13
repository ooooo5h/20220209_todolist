# 플라스크에 적용 가능한 환경설정을 모아두는 클래스
from .my_custom_settings import custom_SQLALCHEMY_DATABASE_URI, AAWS_ACCESS_KEY_ID, AAWS_S3_BUCKET_NAME, AAWS_SECRET_ACCESS_KEY

class Config(object):
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy가 접속할 DB의 연결 정보(URI)
    # 변수이름 바꾸면 X
    SQLALCHEMY_DATABASE_URI = custom_SQLALCHEMY_DATABASE_URI
    
    # DB변경 추적 기능 꺼두기
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # S3 접속 정보로 연결하기
    AWS_ACCESS_KEY_ID = AAWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AAWS_SECRET_ACCESS_KEY
    AWS_S3_BUCKET_NAME = AAWS_S3_BUCKET_NAME
        
class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    
class DebugConfig(Config):
    DEBUG = True