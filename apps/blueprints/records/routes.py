from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from apps.forms.forms import RecordForm
from apps.models.plan import Plans
from apps.models.record import Records
from apps.extentions import db

records_bp = Blueprint('records', __name__, url_prefix='/record')


# 学習記録の一覧画面を表示
@records_bp.route('/list')
@login_required
def list():
    plans = Plans.query.filter_by(user_id = current_user.id)
    records = Records.query.join(Plans).filter(Plans.user_id == current_user.id).all()
    return render_template('records/list.html', plans = plans, records = records)

# 作成機能
@records_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_record():
    record_form = RecordForm()

    # SelectFieldのchoicesを設定
    plans = Plans.query.filter_by(user_id=current_user.id).all()
    record_form.plan.choices = [(p.plan_id, p.title) for p in plans]

    # 学習記録の作成処理
    if record_form.validate_on_submit():
        select_plan_id = record_form.plan.data
        record = Records(plan_id = select_plan_id, title = record_form.title.data, content = record_form.content.data,
                         period = record_form.period.data, product = record_form.product.data, acquired_skills = record_form.acquired_skills.data,
                         reflection = record_form.reflection.data, public_settings = record_form.public_settings.data)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('records.list'))
    else:
        print("FORM ERRORS:", record_form.errors)

    current_app.logger.info(f'{current_user.username} が学習記録を作成しました')
    return render_template('records/create.html', form=record_form)

# 記録の詳細画面
@records_bp.route('/detail/<int:record_id>')
@login_required
def detail_record(record_id):
    record = Records.query.get(record_id)
    return render_template('records/detail.html', record = record)

# 更新機能
@records_bp.route('/update/<int:record_id>', methods=['GET', 'POST'])
@login_required
def update_record(record_id):
    record = Records.query.get(record_id)
    record_form = RecordForm()
    # SelectFieldのchoicesを設定
    plans = Plans.query.filter_by(user_id=current_user.id).all()
    record_form.plan.choices = [(p.plan_id, p.title) for p in plans]

    # 「GET」リクエストの時、Formの初期化
    if request.method == 'GET':
        record_form.process(obj=record)
        # SelectField は手動で代入
        record_form.plan.data = record.plan_id
        return render_template('records/update.html', form = record_form)

    # 「POST」リクエストの時、学習記録の更新処理
    if record_form.validate_on_submit():
        record.plan_id = record_form.plan.data
        record.title = record_form.title.data
        record.content = record_form.content.data
        record.period = record_form.period.data
        record.product = record_form.product.data
        record.acquired_skills = record_form.acquired_skills.data
        record.reflection = record_form.reflection.data
        record.public_settings = record_form.public_settings.data
        db.session.commit()
        current_app.logger.info(f'{current_user.username} が学習記録を更新しました')
        return redirect(url_for('records.list'))
    else:
        print("FORM ERRORS:", record_form.errors)

# 削除機能
@records_bp.route('/delete/<int:record_id>', methods=['GET', 'POST'])
@login_required
def delete_record(record_id):
    record = Records.query.get(record_id)

    # 学習記録の削除処理
    db.session.delete(record)
    db.session.commit()
    current_app.logger.info(f'{current_user.username} が学習記録を削除しました')
    return redirect(url_for('records.list'))