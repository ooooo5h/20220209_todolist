# 플라스크에 적용 가능한 환경설정을 모아두는 클래스

class Config(object):
    DEBUG = False
    TESTING = False
    
class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    
class DebugConfig(Config):
    DEBUG = True