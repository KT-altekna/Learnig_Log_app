from flask import Flask, Blueprint, current_app, request, render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
from apps.forms.forms import ProfileForm
from apps.models.profile import Profiles
from apps.models.user import Users
from werkzeug.utils import secure_filename
from apps.extentions import db
import os

app = Flask(__name__)
# 画像保存先ディレクトリの設定
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, '../../static/uploads')
user_bp = Blueprint('user', __name__, url_prefix='/')

# ユーザーのホーム画面を表示
@user_bp.route('/home')
@login_required
def home():
    return render_template('user/home.html')

# ユーザーのアカウント削除
@user_bp.route('/account/delete/<int:user_id>', methods={'GET', 'POST'})
@login_required
def account_delete(user_id):
    # 「POST」リクエストの時、アカウント削除を実行
    if request.method == 'POST':
        print("POST")
        user = Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        current_app.logger.info(f'アカウントを削除しました')
        return redirect(url_for('auth.top'))
    # 「GET」リクエストの時、アカウント削除画面を表示
    if request.method == 'GET':
        user = Users.query.get(user_id)
        profile = Profiles.query.get(user_id)
        return render_template('user/delete.html', user = user, profile=profile)

# プロフィール情報の詳細を表示
@user_bp.route('/profile/detail/<int:user_id>')
def profile_detail(user_id):
    user = Users.query.get(user_id)
    profile = Profiles.query.get(user_id)
    return render_template('user/detail.html', user = user, profile = profile)

# プロフィール情報の更新処理
@user_bp.route('/profile/update/<int:user_id>', methods={'GET', 'POST'})
@login_required
def profile_update(user_id):
    profile = Profiles.query.get(user_id)
    profile_form = ProfileForm()

    # 「GET」リクエストの時、Formの初期化
    if request.method == 'GET':
        profile_form.process(obj=profile)
        return render_template('user/update.html', form = profile_form)

    # 「POST」リクエストの時、プロフィール情報の更新処理
    if profile_form.validate_on_submit():
        # アイコン画像のURL作成
        if profile_form.icon_image.data:
            image = profile_form.icon_image.data
            filename = secure_filename(image.filename)  # ファイル名を安全に処理
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            # 画像のパスをデータベースに保存
            icon_image_url = f"uploads/{filename}"  # アップロードされた画像のURL
        else:
            icon_image_url = "uploads/noimage.png"

        # プロフィール情報の更新
        profile.icon_image_url = icon_image_url
        profile.gender = profile_form.gender.data
        profile.dob = profile_form.dob.data
        profile.residence = profile_form.residence.data
        profile.occupation = profile_form.occupation.data
        profile.self_intro = profile_form.self_intro.data
        profile.public_settings = profile_form.public_settings.data
        db.session.commit()

        user = Users.query.get(current_user.id)
        current_app.logger.info(f'{current_user.username} がプロフィールを更新しました')
        return redirect(url_for('user.home', username=user.username))
    else:
        print("FORM ERRORS:", profile_form.errors)
