from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func

# ユーザーテーブル
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True) # id
    username=db.Column(db.String(100), unique=True, nullable=False) # ユーザー名
    password=db.Column(db.String(200), nullable=False) # パスワード
    profile = db.relationship('Profiles', backref='user', uselist=False) # プロフィール
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # 作成日時
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # 更新日時

    profile = db.relationship(
        'Profiles',
        backref = 'user',
        cascade = 'all, delete-orphan',
        passive_deletes = True
    )

    favorites = db.relationship(
        'Favorites',
        backref = 'user',
        cascade = 'all, delete-orphan'
    )