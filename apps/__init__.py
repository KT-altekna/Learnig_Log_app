from flask import Flask
from dotenv import load_dotenv
from flask_login import current_user
from apps.errors.handlers import register_error_handlers
from apps.models.profile import Profiles
from apps.extentions import db, login_manager
from apps.logging_config import setup_logging
import os

# .envファイルを呼び込む
load_dotenv()

# アプリケーションの初期化
def create_app():
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('apps.config.ProductionConfig')
    else:
        app.config.from_object('apps.config.DevelopmentConfig')

    # secret_keyをランダム生成(※本番環境では.envファイルで定義)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # DB, 拡張機能の初期化
    db.init_app(app)
    login_manager.init_app(app)

    # プロフィール情報をテンプレート内で常に利用可能にする
    @app.context_processor
    def inject_profile():
        if current_user.is_authenticated:
            profile = Profiles.query.filter_by(user_id=current_user.id).first()
            return dict(current_profile=profile)
        return dict(current_profile=None)

    register_error_handlers(app)
    setup_logging(app)
    return app

