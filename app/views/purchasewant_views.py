from flask import Blueprint, request, jsonify
from app import db
from app.models import Post
bp = Blueprint('purchasewant', __name__, url_prefix='/purchasewant')
#@bp.route('/purchasewant', methods=['POST'])
@bp.route('', methods=['POST'])
def submit_purchase():
    data = request.json
    post_id = data.get('post_id')

    # 데이터베이스에서 post_id에 해당하는 상품 정보를 가져옴
    post = db.session.query(Post).filter_by(id=post_id).first()  # Post로 수정

    if post:
        # 필요한 데이터만 반환
        response_data = {
            'title': post.title,
            'content': post.content,
            'price': post.price,
            # 추가 데이터가 필요하다면 여기에 추가
        }
        return jsonify({'success': True, 'data': response_data})
    return jsonify({'success': False, 'message': '상품을 찾을 수 없습니다.'})