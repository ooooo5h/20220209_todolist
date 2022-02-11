# todolist의 is_completed를 완료로 변경하면 자동으로 db에 저장되게 해보고 싶다.
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db

class Done(Resource):
    
    # to do list에서 done으로생성하기
    def post(self):
        
        # todo의 id를 입력하면, 그 id가 todolist에 존재하는지? 없다면 없는 번호라고 리턴
        # id가 todolist에 존재하면, is_completed가 yes인지 확인하고
        # yes라면 dones에 추가하면 될 것 같은데 일단 주석만 작성
        return {
            'code' : '임시 생성하기'
        }