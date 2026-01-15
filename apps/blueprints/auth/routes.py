from flask import Flask, Blueprint, flash, render_template, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from apps.forms.forms import UserForm, ProfileForm
from apps.models.user import Users
from apps.models.profile import Profiles
from werkzeug.utils import secure_filename
from apps.extentions import db
import os

app = Flask(__name__)
# 画像保存先ディレクトリの設定
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, '../../static/uploads')
auth_bp = Blueprint('auth', __name__, url_prefix='/')

# アプリのトップ画面を表示
@auth_bp.route('/')
def top():
    return render_template('auth/top.html')

# ログイン機能
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    user_form = UserForm()
    if user_form.validate_on_submit():
        username = user_form.user.data
        password = user_form.password.data
        user = Users.query.filter_by(username=username).first()
        if user == None:
            flash('ユーザーが登録されていません。ユーザー名を修正するか、新規登録してください。')
            return redirect('/login')
        if check_password_hash(user.password, password=password):
            login_user(user)
            current_app.logger.info(f'{current_user.username} がログインしました')
            return redirect(url_for('user.home'))
        else:
            flash('パスワードが違います。正しいパスワードを入力してください。')
            return redirect('/login')
    else:
        print("FORM ERRORS:", user_form.errors)

    return render_template('auth/login.html', form=user_form)

# サインアップ機能
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    user_form = UserForm()
    profile_form = ProfileForm()
    if user_form.validate_on_submit():
        # Usersテーブルにデータを作成
        username = user_form.user.data
        hashed_pass = generate_password_hash(user_form.password.data)
        user = Users(username = username, password = hashed_pass)
        db.session.add(user)
        db.session.commit()

        # Profileテーブルにデータを作成
        user = Users.query.order_by(Users.id.desc()).first()
        if profile_form.icon_image.data:
            image = profile_form.icon_image.data
            filename = secure_filename(image.filename)  # ファイル名を安全に処理
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            # 画像のパスをデータベースに保存
            icon_image_url = f"uploads/{filename}"  # アップロードされた画像のURL
        else:
            icon_image_url = "uploads/noimage.png"

        profile = Profiles(user_id = user.id, icon_image_url = icon_image_url, gender = profile_form.gender.data,
                            dob = profile_form.dob.data, residence = profile_form.residence.data, occupation = profile_form.occupation.data,
                            self_intro = profile_form.self_intro.data, public_settings = profile_form.public_settings.data)
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        current_app.logger.info(f'{current_user.username} がログインしました')
        return redirect(url_for('user.home'))
    else:
        print("FORM ERRORS:", user_form.errors)

    return render_template('auth/signup.html', user_form=user_form, profile_form=profile_form)

# ログアウト機能
@auth_bp.route('/logout')
def logout():
    current_app.logger.info(f'{current_user.username} がログアウトしました')
    logout_user()
    return render_template('auth/top.html')