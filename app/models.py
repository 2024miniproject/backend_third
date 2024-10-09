from app import db  # db 인스턴스를 가져옵니다.
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    content = db.Column(db.Text)
    filename = db.Column(db.String(200))
    image_filename = db.Column(db.String(200), nullable=True)

    def __init__(self, title, price, content, filename, image_filename=None):
        self.title = title
        self.price = price
        self.content = content
        self.filename = filename
        self.image_filename = image_filename

    def __repr__(self):
        return f'<Post {self.title}>'


class StatusEnum(Enum):
    PENDING = '대기중'
    PAYMENT_COMPLETED = '입금완료'
    SIZE_SELECTED = '사물함크기선택완료'
    LOCKER_ASSIGNED = '사물함배치완료'
    TRANSACTION_COMPLETED = '거래완료'

class buy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)  # 상태를 Enum으로 정의
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)  # 상태를 Enum으로 정의
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 사용자 외래키
    user = relationship('User', backref='comments')  # 사용자와의 관계 정의
    username = db.Column(db.Text, nullable=False)
    #question_id = db.Column(db.Integer, db.ForeignKey('question.id'))  # 질문 외래키

    def __repr__(self):
        return f'<Comment {self.content}>'
