from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func, CheckConstraint

# 学習計画テーブル
class Plans(UserMixin, db.Model):
    __tablename__ = 'plans'
    plan_id=db.Column(db.Integer, primary_key=True, autoincrement=True) # 計画id(主キー)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE')) # ユーザーid(外部キー)
    title=db.Column(db.String(100), nullable=False) # タイトル名
    purpose = db.Column(db.String(500), nullable=False) # 学習目的
    start_date = db.Column(db.Date, nullable=False) # 開始日
    final_date = db.Column(db.Date, nullable=False) # 終了日
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # 作成日時
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # 更新日時

    # CHECK制約を定義
    __table_args__ = (
        CheckConstraint('final_date >= start_date', name='period_check'),
    )