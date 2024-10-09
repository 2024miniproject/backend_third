import os

# 현재 파일 경로를 기준으로 BASE_DIR 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db'))+ '?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 개발용 SECRET_KEY
SECRET_KEY = "dev"

# 이미지 업로드를 위한 폴더 경로 설정

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')  # 'static/uploads' 폴더 경로


import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# 'uploads' 폴더가 없을 경우 자동으로 생성되도록 처리
#if not os.path.exists(UPLOAD_FOLDER):
 #   os.makedirs(UPLOAD_FOLDER)
