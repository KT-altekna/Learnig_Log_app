from apps import create_app
from apps.extentions import db,login_manager
from apps.blueprints.auth.routes import auth_bp
from apps.blueprints.user.routes import user_bp
from apps.blueprints.plans.routes import plans_bp
from apps.blueprints.records.routes import records_bp
from apps.blueprints.public.routes import public_bp
from apps.blueprints.favorite.routes import favorite_bp
from apps.models.user import Users
from flask_migrate import Migrate

# インスタンス生成
app = create_app()

# ユーザー識別用の関数
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

# blueprintを登録
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(records_bp)
app.register_blueprint(public_bp)
app.register_blueprint(favorite_bp)

# Migrateとアプリ連携
Migrate(app, db)

# アプリの起動
if __name__=="__main__":

    app.run(debug=True)
