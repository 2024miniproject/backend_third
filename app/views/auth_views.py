import functools

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db
from app.forms import UserCreateForm, UserLoginForm
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)



@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        femail = form.email.data  # username 대신 email로 변경했다면 email로 사용
        password = form.password.data

        # 데이터베이스에서 유저 조회
        user = User.query.filter_by(email=femail).first()

        # 유저가 존재하고 비밀번호가 일치하는지 확인
        if user is None:
            flash("존재하지 않는 사용자입니다.", 'danger')
        elif not check_password_hash(user.password, password):
            flash("비밀번호가 올바르지 않습니다.", 'danger')
        else:
            # 세션에 유저 정보를 저장하고 홈 화면으로 리디렉션
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('home_views.home'))

    return render_template('front/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)

    return wrapped_view
