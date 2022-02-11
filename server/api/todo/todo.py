from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

put_parser = reqparse.RequestParser()
put_parser.add_argument('user_id', type=int, required=True, location='form')
put_parser.add_argument('title', type=str, required=True, location='form')
put_parser.add_argument('content', type=str, required=True, location='form')
put_parser.add_argument('duedate', type=str, required=True, location='form')


class Todo(Resource):
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do list 생성하기',
        'parameters' : [
            {
                'name' : 'user_id',
                'description' : '사용자의 id',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True,
            },
            {
                'name' : 'title',
                'description' : 'to do list 제목',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'content',
                'description' : 'to do list 내용',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
            {
                'name' : 'duedate',
                'description' : '데드라인 날짜',
                'in' : 'formData',
                'type' : 'string',
                # 'format' : 'date',
                'required' : True,
            },
        ],
        'responses' : {
            '200' : {
                'description' : 'to do list 생성 성공' 
            },
            '400' : {
                'description' : 'to do list 생성 실패' 
            },    
        }
    })
    def put(self):
        """to do list를 생성합니다."""
        
        return {
            '임시' : '임시 투두 겟'
        }