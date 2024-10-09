from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models import Post, db
import os
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('write_views', __name__)

@bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        content = request.form['content']

        # 파일 업로드 처리
        files = request.files.getlist('files')  # 여러 파일 업로드 지원
        filenames = []
        image_filename = None  # 이미지 파일명을 저장할 변수 추가

        upload_folder = current_app.config['UPLOAD_FOLDER']  # 업로드 폴더 가져오기
        if not os.path.exists(upload_folder):  # 폴더가 없으면 생성
            os.makedirs(upload_folder)

        for file in files:
            if file and file.filename:  # 파일이 존재하고, filename이 비어있지 않은 경우
                filename = secure_filename(file.filename)  # 파일 이름을 안전하게 변환
                unique_filename = f"{uuid.uuid4().hex}_{filename}"  # 고유 파일명 생성
                save_path = os.path.join(upload_folder, unique_filename)
                file.save(save_path)  # 파일 저장
                filenames.append(unique_filename)  # 저장된 파일 이름을 리스트에 추가
                if not image_filename:  # 첫 번째 파일을 이미지 파일로 간주
                    image_filename = unique_filename

        # 이미지 파일 경로는 'static/uploads/파일명' 형태로 저장
        image_path = f"uploads/{image_filename}"

        # 데이터베이스에 포스트 추가
        try:
            new_post = Post(title=title, price=price, content=content, filename=', '.join(filenames),
                            image_filename=image_path)
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # 롤백
            return "오류가 발생했습니다. 다시 시도해주세요.", 500

        # 성공 메시지 후 홈 화면으로 리다이렉트
        return '''
        <script>
            alert("등록이 완료되었습니다.");
            window.location.href = "{url}";
        </script>
        '''.format(url=url_for('home_views.home'))  # 홈 화면으로 리다이렉트

    return render_template('front/write.html')

@bp.route('/information/write.html')
def information_write():
    return render_template('front/write.html')  # 필요한 템플릿을 반환합니다.
