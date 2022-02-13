from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from werkzeug.datastructures import FileStorage
from flask import current_app
import boto3

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
            
            # 파일에는 파일이름과 본문이 있음
            file_name = file.filename
            s3_file_path = f'images/todo_imgs/{file_name}' # 파일 이름은 올라갈 경로를 생성할 때 활용
            
            # 본문은 실제로 올려줄 파일에 해당됨
            file_body = file.stream.read()
            
            # 어떤 버킷에 올려줄건지 버킷이름을 꺼내고, 저장해줄 이름과 파일을 put해줌
            aws_s3.Bucket(current_app.config['AWS_S3_BUCKET_NAME']).put_object(Key=s3_file_path, Body=file_body)
            
            # ACL을 퍼블릭 허용으로 설정해줘야함
            aws_s3.ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_path).put(ACL='public-read')
            
        
        return {
            'code' : 'to do 이미지 등록하는 기능' 
        }