# 플라스크에 적용 가능한 환경설정을 모아두는 클래스
from .my_custom_settings import custom_SQLALCHEMY_DATABASE_URI
class Config(object):
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy가 접속할 DB의 연결 정보(URI)
    # 변수이름 바꾸면 X
    SQLALCHEMY_DATABASE_URI = custom_SQLALCHEMY_DATABASE_URI
    
    # DB변경 추적 기능 꺼두기
    SQLALCHEMY_TRACK_MODIFICATIONS = False
        
class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    
class DebugConfig(Config):
    DEBUG = True