from flask import Blueprint, request, jsonify
from app import db
from app.models import Comment, User # 필요한 모델 임포트
from datetime import datetime
from flask import session
from app.models import Post  # Post 모델 임포트
from flask import render_template  # render_template 임포트


bp = Blueprint('comment', __name__, url_prefix='/')


@bp.route('/detail/<int:post_id>')  # 게시글 상세 보기
def detail(post_id):
    post = Post.query.get_or_404(post_id)  # 주어진 post_id에 해당하는 게시글 가져오기
    return render_template('front/detail.html', post=post)  # 게시글 데이터를 템플릿에 전달

@bp.route('/add_comment', methods=['POST'])  # 댓글 추가 엔드포인트
def add_comment():
    data = request.get_json()  # JSON 데이터 받아오기
    comment_text = data.get('comment')
    user_id = 1  # 실제 사용자 ID는 세션이나 인증 정보를 통해 가져와야 함 (예시로 1을 설정)
    question_id = 1  # 질문 ID를 실제 데이터에 맞게 설정

    if comment_text and user_id and question_id:
        new_comment = Comment(
            content=comment_text,
            created_at=datetime.utcnow(),
            user_id=user_id,
            username='익명',  # 실제 사용자 이름으로 대체해야 함
            question_id=question_id
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@bp.route('/get_comments/<int:question_id>', methods=['GET'])
def get_comments(question_id):
    comments = Comment.query.filter_by(question_id=question_id).all()  # 해당 질문의 댓글만 필터링
    comment_list = []
    for comment in comments:
        comment_list.append({
            'username': comment.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat()
        })
    return jsonify(comment_list)

