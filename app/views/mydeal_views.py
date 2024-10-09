from flask import render_template, request
from app.models import buy, sell
from flask import Blueprint

bp = Blueprint('mydeal', __name__, url_prefix='/mydeal_views')
# 구매 목록 라우트
@bp.route('/mydealbuy')
def mydealbuy():
    # 데이터베이스에서 구매 데이터 가져오기
    purchase_list = buy.query.all()
    return render_template('front/mydealbuy.html', purchases=purchase_list)

# 판매 목록 라우트
@bp.route('/mydealsell')
def mydealsell():
    # 데이터베이스에서 판매 데이터 가져오기
    sale_list = sell.query.all()
    return render_template('front/mydealsell.html', sales=sale_list)