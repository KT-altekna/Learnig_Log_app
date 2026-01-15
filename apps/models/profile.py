from flask_login import UserMixin
from apps.extentions import db
from sqlalchemy import func

# プロフィールテーブル
class Profiles (UserMixin, db.Model):
    __tablename__ = 'profile'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True) # id(主キー&外部キー)
    icon_image_url = db.Column(db.String(255)) # アイコン画像
    gender = db.Column(db.String(10)) # 性別
    dob = db.Column(db.Date) # 生年月日
    residence = db.Column(db.String(50)) # 居住地
    occupation = db.Column(db.String(50)) # 職業
    self_intro = db.Column(db.String(500)) # 自己紹介
    public_settings = db.Column(db.Boolean, default=False) # 公開設定
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # 更新日時