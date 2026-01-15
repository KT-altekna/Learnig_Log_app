from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from apps.models.plan import Plans
from apps.models.profile import Profiles
from apps.models.record import Records
from apps.models.user import Users
from apps.models.favorite import Favorites
from apps.extentions import db

favorite_bp = Blueprint('favorite', __name__, url_prefix='/favorite')

# 公開記録のお気に入り登録
@favorite_bp.route('/add/<int:record_id>')
@login_required
def favorite_add(record_id):
    exists = Favorites.query.filter_by(
        user_id=current_user.id,
        record_id=record_id
    ).first()

    if not exists:
        favorite = Favorites(
            user_id=current_user.id,
            record_id=record_id
        )
        db.session.add(favorite)
        db.session.commit()

    return redirect(request.referrer)

# 公開記録のお気に入り解除
@favorite_bp.route('/remove/<int:record_id>')
@login_required
def favorite_remove(record_id):
    favorite = Favorites.query.filter_by(
        user_id=current_user.id,
        record_id=record_id
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    return redirect(request.referrer)

# 公開記録のお気に入り一覧
@favorite_bp.route('/list')
@login_required
def favorite_list():
    records = (db.session.query(Records, Users, Profiles)
                .join(Favorites, Favorites.record_id == Records.record_id)
                .join(Plans, Records.plan_id == Plans.plan_id)
                .join(Users, Plans.user_id == Users.id)
                .join(Profiles, Profiles.user_id == Users.id)
                .filter(
                    Favorites.user_id == current_user.id,
                    Records.public_settings == True
                )
                .order_by(Records.created_at.desc())
                .all())

    return render_template('favorite/list.html', records = records)