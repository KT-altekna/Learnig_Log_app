from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func

# 学習記録テーブル
class Records(UserMixin, db.Model):
    __tablename__ = 'records'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 記録id(主キー)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id', ondelete='CASCADE')) # 計画id(外部キー)
    title = db.Column(db.String(100), nullable=False) # タイトル名
    content = db.Column(db.String(500), nullable=False) # 学習内容
    period = db.Column(db.String(100), nullable=False) # 学習時間
    product = db.Column(db.String(500)) # 成果物
    acquired_skills = db.Column(db.String(1000)) # 身についた技術
    reflection = db.Column(db.String(1000)) # 振り返り
    public_settings = db.Column(db.Boolean, default=True) # 公開設定
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # 作成日時
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # 更新日時

    favorites = db.relationship(
        'Favorites',
        backref = 'record',
        cascade = 'all, delete-orphan'
    )