from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Post
import os

bp = Blueprint('write_views', __name__)

@bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        content = request.form['content']
        files = request.files.getlist('files')

        # 파일 저장 로직
        image_filenames = []
        for file in files:
            if file:
                filename = file.filename
                file.save(os.path.join('uploads/', filename))
                image_filenames.append(filename)

        # 판매글 데이터베이스에 저장
        new_post = Post(title=title, price=price, content=content, image_filename=', '.join(image_filenames))
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home_views.home'))  # 홈으로 리다이렉트

    return render_template('front/home2.html')  # GET 요청 시 홈 페이지 렌더링
