from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from flask import g
from server import db
from server.api.utils import token_required
from server.model import Todos

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')
post_parser.add_argument('duedate', type=str, required=True, location='form')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('todo_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('todo_id', type=int, required=True, location='args')

class Todo(Resource):
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do list 생성하기',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '사용자의 토큰',
                'in' : 'header',
                'type' : 'string',
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
    @token_required
    def post(self):
        """to do list 생성하기"""
        
        # 존재하는 사용자일 때 처리하기
        args = post_parser.parse_args()
        user = g.user
        
        create_todo = Todos()
        create_todo.user_id = user.id
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
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do list 수정하기',
        'parameters' : [
            {
                'name' : 'todo_id',
                'description' : '수정하고자 하는 to do list의 번호',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True,
            },
            {
                'name' : 'field',
                'description' : '수정하고 싶은 항목',
                'in' : 'formData',
                'type' : 'string',
                'enum' : ['title', 'content', 'duedate', 'is_completed'],
                'required' : True,
            },
            {
                'name' : 'value',
                'description' : '수정할 값',
                'in' : 'formData',
                'type' : 'string',
                'required' : True,
            },
        ],
        'responses' : {
            '200' : {
                'description' : 'to do list 수정 성공'
            },
            '400' : {
                'description' : 'to do list 수정 실패'
            }
        }
    })    
    def patch(self):
        """to do list 수정하기"""
        
        args = patch_parser.parse_args()
        
        # 실존하는 to do list의 아이디인가?
        exist_todo_id = Todos.query.filter(Todos.id == args['todo_id']).first()
        
        if not exist_todo_id:
            return {
                'code' : 400,
                'message' : '존재하지 않는 to do list의 번호입니다.'
            }, 400
            
        else :
            # 수정하고자 하는 to do list의 번호가 있다면,
            # 1. 제목 수정
            if args['field'] == 'title':
                exist_todo_id.title = args['value']
                db.session.add(exist_todo_id)
                db.session.commit()
                
                return {
                    'code' : 200,
                    'message' : '제목 수정 완료'
                }
            # 2. 내용 수정    
            elif args['field'] == 'content':
                exist_todo_id.content = args['value']
                db.session.add(exist_todo_id)
                db.session.commit()
                
                return {
                    'code' : 200,
                    'message' : '내용 수정 완료'
                }
            # 3. 마감일자 수정    
            elif args['field'] == 'duedate':
                exist_todo_id.duedate = args['value']
                db.session.add(exist_todo_id)
                db.session.commit()
                
                return {
                    'code' : 200,
                    'message' : '마감일자 수정 완료'
                }
            # 4. 완료여부 수정    
            if args['field'] == 'is_completed':
                exist_todo_id.is_completed = int(args['value'])
                db.session.add(exist_todo_id)
                db.session.commit()
                
                return {
                    'code' : 200,
                    'message' : '완료여부 수정 완료'
                }

    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do list 삭제하기',
        'parameters' : [
            {
                'name' : 'todo_id',
                'description' : '삭제할 to do 의 번호',
                'in' : 'query',
                'type' : 'integer',
                'required' : True,
            }
        ],
        'responses' : {
            '200' : {
                'description' : '삭제 성공'
            },
            '400' : {
                'description' : '삭제 실패'
            }
        }
    })
    def delete(self):
        """to do list 삭제하기"""
        
        args = delete_parser.parse_args()
        
        # 실존하는 to do  번호인가
        exist_todo_id = Todos.query.filter(Todos.id == args['todo_id']).first()
        if not exist_todo_id:
            return {
                'code' : 400,
                'message' : '존재하지 않는 to do 의 번호입니다.'
            }, 400
        
        db.session.delete(exist_todo_id)
        db.session.commit()
        
        return {
            'code' : 200,
            'message' : 'to do list 삭제 성공'
        }
        
    @swagger.doc({
        'tags' : ['todo'],
        'description' : '모든 to do list 조회하기',
        'parameters' : [
        ],
        'responses' : {
            '200' : {
                'description' : '조회 성공'
            },
            '400' : {
                'description' : '조회 실패'
            }
        }
    })    
    def get(self):
        """모든 to do list 조회하기"""
        
        all_to_do = Todos.query.all()
        
        to_do_list = [todo.get_data_object() for todo in all_to_do]
        
        return {
            'code' : 200,
            'message' : '모든 to do list 조회 성공',
            'data' : {
                'todos' : to_do_list,
            }
        }