from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func

# マイルストーンテーブル
class Milestones(UserMixin, db.Model):
    __tablename__ = 'milestones'
    milestone_id=db.Column(db.Integer, primary_key=True, autoincrement=True) # マイルストーンid(主キー)
    plan_id=db.Column(db.Integer, db.ForeignKey("plans.plan_id", ondelete='CASCADE')) # 計画id(外部キー)
    title=db.Column(db.String(100), nullable=False) # タイトル名
    due_date=db.Column(db.Date, nullable=False) # 締切日
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # 作成日時
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # 更新日時