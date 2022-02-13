from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from werkzeug.datastructures import FileStorage
from flask import current_app
import boto3
import time
import os

from server.model import Users

put_parser = reqparse.RequestParser()
put_parser.add_argument('image_file', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('todo_id', type=int, required=True, location='form')

class TodoImage(Resource):
    
    @swagger.doc({
        'tags' : ['todo'],
        'description' : 'to do 이미지 등록하기',
        'parameters' : [
            {
                'name' : 'todo_id',
                'description' : '사진을 첨부할 todo의 id',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True,
            },
            {
                'name' : 'image_file',
                'description' : '실제로 첨부할 이미지 파일',
                'in' : 'formData',
                'type' : 'file',
                'required' : True,
            }
        ],
        'responses' : {
            '200' : {
                'description' : '사진 첨부 성공'
            },
            '400' : {
                'description' : '사진 첨부 실패'
            },
        }
    })
    def put(self):
        """to do 이미지 등록하는 기능"""
        
        args = put_parser.parse_args()
        
        aws_s3 = boto3.resource('s3',\
            aws_access_key_id = current_app.config['AWS_ACCESS_KEY_ID'],\
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
        
        for file in args['image_file']:
            
            # 파일이름을 첨부한 이름 그대로 사용하면, 중복 발생의 소지가 있어서 '누가_언제'올렸는지로 재가공하고 확장자는 그대로 가져다 사용한다
            # 먼저 파일 이름 재가공은 아래처럼 실시
            user_nickname = 'test' 
            now = round(time.time()*10000) # 중복을 피하기 위한 요소로, 현재 시간을 간단한 숫자값으로 표현하자
            
            new_file_name = f"TODOLIST_{user_nickname}_{now}"
            
            # 원래 올라온 파일명을 파일이름과 확장자로 분리하여 확장자만 추출
            _, file_extension = os.path.splitext(file.filename)
            new_file_name = f"{new_file_name}{file_extension}"
    
            s3_file_path = f'images/todo_imgs/{new_file_name}' # 파일 이름은 올라갈 경로를 생성할 때 활용
            
            # 본문은 실제로 올려줄 파일에 해당됨
            file_body = file.stream.read()
            
            # 어떤 버킷에 올려줄건지 버킷이름을 꺼내고, 저장해줄 이름과 파일을 put해줌
            aws_s3.Bucket(current_app.config['AWS_S3_BUCKET_NAME']).put_object(Key=s3_file_path, Body=file_body)
            
            # ACL을 퍼블릭 허용으로 설정해줘야함
            aws_s3.ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_path).put(ACL='public-read')
            
        
        return {
            'code' : 'to do 이미지 등록하는 기능' 
        }