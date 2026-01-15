from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from apps.forms.forms import PlanForm, MilestoneForm
from apps.models.plan import Plans
from apps.models.milestone import Milestones
from apps.extentions import db

plans_bp = Blueprint('plans', __name__, url_prefix='/plan')

# 学習計画の一覧画面を表示
@plans_bp.route('/list')
@login_required
def list():
    plans = Plans.query.filter_by(user_id = current_user.id)
    milestones = Milestones.query.all()
    return render_template('plans/list.html', plans = plans, milestones = milestones)

# 作成機能
@plans_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_plan():
    plan_form = PlanForm()
    # 「マイルストーン追加」押されたときだけ、行追加して再表示
    if plan_form.add_milestone.data:
        plan_form.milestones.append_entry()
        return render_template('plans/create.html', form=plan_form)
    # マイルストーン一覧で「削除」押されると、該当するマイルストーンを削除して再表示
    for i, ms in enumerate(plan_form.milestones.entries):
        if ms.form.remove_milestone.data:
            del plan_form.milestones.entries[i]
            return render_template('plans/create.html', form=plan_form)

    # 学習計画の作成処理
    if plan_form.validate_on_submit():
        plan = Plans(user_id = current_user.id, title = plan_form.title.data, purpose = plan_form.purpose.data,
                    start_date = plan_form.start_date.data, final_date = plan_form.final_date.data)
        db.session.add(plan)
        db.session.commit()
        if plan_form.milestones.data:
            for ms in plan_form.milestones.entries:
                milestone = Milestones(plan_id = plan.plan_id, title = ms.form.title.data, due_date = ms.form.due_date.data)
                db.session.add(milestone)
                db.session.commit()
        # 保存完了
        current_app.logger.info(f'{current_user.username} が学習計画を作成しました')
        return redirect(url_for('plans.list'))
    else:
        print("FORM ERRORS:", plan_form.errors)

    return render_template('plans/create.html', form=plan_form)

# 計画の詳細画面
@plans_bp.route('/detail/<int:plan_id>')
@login_required
def detail_plan(plan_id):
    plan = Plans.query.get(plan_id)
    milestones= Milestones.query.filter_by(plan_id = plan_id)
    return render_template('plans/detail.html', plan = plan, milestones = milestones)

# 更新機能
@plans_bp.route('/update/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def update_plan(plan_id):
    milestones= Milestones.query.filter_by(plan_id = plan_id).all()
    plan = Plans.query.get(plan_id)

    # 「GET」リクエストの時だけ、Form初期化
    if request.method == 'GET':
        plan_form = PlanForm(obj=plan)
        plan_form.milestones.entries = []
        for ms in milestones:
            entry_form = MilestoneForm()
            entry_form.milestone_id.data = ms.milestone_id
            entry_form.title.data = ms.title
            entry_form.due_date.data = ms.due_date
            plan_form.milestones.append_entry(entry_form.data)
        return render_template('plans/update.html', form=plan_form)

    # 「POST」リクエストの時（更新時）
    plan_form = PlanForm()

    # 「マイルストーン追加」押されたときだけ、行追加して再表示
    if plan_form.add_milestone.data:
        plan_form.milestones.append_entry()
        return render_template('plans/update.html', form=plan_form)
    # マイルストーン一覧で「削除」押されると、該当するマイルストーンを削除して再表示
    for i, ms in enumerate(plan_form.milestones.entries):
        if ms.form.remove_milestone.data:
            del plan_form.milestones.entries[i]
            return render_template('plans/update.html', form=plan_form)

    # 学習計画の更新処理
    if plan_form.validate_on_submit():
        # 計画本体の更新
        plan.title = plan_form.title.data
        plan.purpose = plan_form.purpose.data
        plan.start_date = plan_form.start_date.data
        plan.final_date = plan_form.final_date.data

        # マイルストーンの更新または追加
        valid_ids = []
        for ms in plan_form.milestones.entries:
            if ms.form.milestone_id.data:
                milestone = Milestones.query.get(ms.form.milestone_id.data)
                milestone.title = ms.form.title.data
                milestone.due_date = ms.form.due_date.data
                valid_ids.append(milestone.milestone_id)
            else:
                new_ms = Milestones(plan_id = plan.plan_id, title = ms.form.title.data, due_date = ms.form.due_date.data)
                db.session.add(new_ms)
                db.session.commit()
                valid_ids.append(new_ms.milestone_id)
        db.session.commit()

        # マイルストーンを削除した場合、DBのレコードを削除
        db_milestones = Milestones.query.filter_by(plan_id=plan_id).all()
        for db_ms in db_milestones:
            if db_ms.milestone_id not in valid_ids:
                db.session.delete(db_ms)
        db.session.commit()

        # 保存完了
        return redirect(url_for('plans.list'))
    else:
        print("FORM ERRORS:", plan_form.errors)

    current_app.logger.info(f'{current_user.username} が学習計画を更新しました')
    return render_template('plans/update.html', form = plan_form)

# 削除機能
@plans_bp.route('/delete/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def delete_plan(plan_id):
    plan = Plans.query.get(plan_id)

    # 学習計画の削除処理
    db.session.delete(plan)
    db.session.commit()
    current_app.logger.info(f'{current_user.username} が学習計画を削除しました')
    return redirect(url_for('plans.list'))