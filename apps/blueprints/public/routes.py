from flask import Blueprint, render_template
from flask_login import current_user
from apps.models.favorite import Favorites
from apps.models.plan import Plans
from apps.models.profile import Profiles
from apps.models.record import Records
from apps.models.user import Users
from apps.extentions import db

public_bp = Blueprint('public', __name__, url_prefix='/public')

# 公開記録の一覧画面を表示
@public_bp.route('/list')
def public_list():
    records = (db.session.query(Records, Users, Profiles)
                .join(Plans, Records.plan_id == Plans.plan_id)
                .join(Users, Plans.user_id == Users.id)
                .join(Profiles, Profiles.user_id == Users.id)
                .filter(
                    Records.public_settings == True
                )
                .order_by(Records.created_at.desc())
                .all())
    return render_template('public/list.html', records = records)

# 公開記録の詳細画面を表示
@public_bp.route('/detail/<int:record_id>')
def public_detail(record_id):
    record = Records.query.get(record_id)
    plan = Plans.query.get(record.plan_id)

    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = (Favorites.query.
                    filter_by(user_id = current_user.id, record_id = record.record_id).
                    first()
                    is not None)
    return render_template('public/detail.html', plan = plan, record = record, is_favorite = is_favorite)



