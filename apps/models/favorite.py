from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func

# お気に入り登録テーブル
class Favorites(UserMixin, db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True) # ユーザーid（主キー&外部キー）
    record_id = db.Column(db.Integer, db.ForeignKey("records.record_id", ondelete='CASCADE'), primary_key=True) # 記録id（主キー＆外部キー）
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # 作成日時

    __table_args__ = (
        db.UniqueConstraint('user_id', 'record_id', name = 'uq_user_record'),
    )