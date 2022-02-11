from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server.model.users import Users
from server import db

from server.model import Todos

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, required=True, location='form')
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')
post_parser.add_argument('duedate', type=str, required=True, location='form')


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
    def post(self):
        """to do list를 생성합니다."""
        
        # # 존재하는 사용자일 때 처리하기
        args = post_parser.parse_args()
        exist_user = Users.query.filter(Users.id == args['user_id']).first()
        
        if not exist_user:
            return {
                'code' : 400,
                'message' : '존재하지 않는 사용자의 번호입니다.'
            }, 400
        
        create_todo = Todos()
        create_todo.user_id = args['user_id']
        create_todo.title = args['title']
        create_todo.content = args['content']
        create_todo.duedate = args['duedate']
        
        db.session.add(create_todo)
        db.session.commit()       
        
        return {
            'code' : '200',
            'message' : 'to do list 생성완료',
            'data' : {
                'feed' : create_todo.get_data_object(),
            }
        }