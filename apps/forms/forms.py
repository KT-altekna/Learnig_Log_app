from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, FieldList, FormField, SubmitField, StringField, DateField, PasswordField, SelectField, TextAreaField, BooleanField, RadioField, HiddenField
from wtforms.validators import DataRequired, Optional, Length

class UserForm(FlaskForm):
    user = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])

    signup_submit = SubmitField('新規登録')
    login_submit = SubmitField('ログイン')

class ProfileForm(FlaskForm):
    icon_image = FileField('アイコン画像', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'ico'], '画像ファイルのみ許可されています')])
    gender = RadioField('性別', validators=[Optional()], choices=[('男', '男性'), ('女','女性')])
    dob = DateField('生年月日', validators=[Optional()], format='%Y-%m-%d')
    residence = StringField('居住地', validators=[Optional()])
    occupation = StringField('職業', validators=[Optional()])
    self_intro = TextAreaField('自己紹介', validators=[Optional(), Length(max=500)])
    public_settings = BooleanField('公開設定', render_kw={'class': 'form-checkbox'})

    update_submit = SubmitField('更新')

class MilestoneForm(FlaskForm):
    milestone_id = HiddenField()
    title = StringField('タイトル', validators=[Optional()])
    due_date = DateField('期限', validators=[Optional()])

    remove_milestone = SubmitField('削除')

class PlanForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    purpose = StringField('学習目的', validators=[DataRequired()])
    start_date = DateField('開始日', validators=[DataRequired()])
    final_date = DateField('終了日', validators=[DataRequired()])

    # マイルストーンを複数個持てるようにする
    milestones = FieldList(
        FormField(MilestoneForm)
    )

    add_milestone = SubmitField('マイルストーンを追加')
    create_submit = SubmitField('作成')
    update_submit = SubmitField('更新')

class RecordForm(FlaskForm):
    plan = SelectField(
        '学習計画',
        coerce=int,
        validators=[DataRequired()]
    )
    title = StringField('タイトル', validators=[DataRequired()])
    content = StringField('学習内容', validators=[DataRequired()])
    period = StringField('学習時間', validators=[DataRequired()])
    product = TextAreaField('成果物', validators=[Optional(), Length(max=300)])
    acquired_skills = TextAreaField('身についた技術', validators=[Optional(), Length(max=300)])
    reflection = TextAreaField('振り返り', validators=[Optional(), Length(max=300)])
    public_settings = BooleanField('公開設定', render_kw={'class': 'form-checkbox'})

    create_submit = SubmitField('作成')
    update_submit = SubmitField('更新')