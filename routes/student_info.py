from flask import Blueprint, render_template, request, redirect, url_for
from models import Student_info as si
from peewee import fn

# Blueprintの作成
student_info_bp = Blueprint('student_info', __name__, url_prefix='/student_infos')


@student_info_bp.route('/')
def list():

    # データ取得
    student_info = si.select()
    count_male = si.select(fn.COUNT(si.id)).where(si.sex == "男").scalar() or 0
    count_female = si.select(fn.COUNT(si.id)).where(si.sex == "女").scalar() or 0
    count_other = si.select(fn.COUNT(si.id)).where(si.sex == "その他").scalar() or 0

    return render_template(
        'student_info_list.html',
        title='学籍情報一覧',
        items=student_info,
        m_sum=count_male,
        f_sum=count_female,
        o_sum=count_other
    )

@student_info_bp.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        sex = request.form['sex']
        age = request.form['age']
        si.create(id=id,name=name,sex=sex,age=age)
        return redirect(url_for('student_info.list'))

    return render_template('student_info_add.html')


@student_info_bp.route('/edit/<string:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    student_info = si.get_or_none(si.id == student_id)
    if not student_info:
        return redirect(url_for('.list'))

    if request.method == 'POST':
        student_info.id = request.form['id']
        student_info.name = request.form['name']
        student_info.sex = request.form['sex']
        student_info.age = request.form['age']
        student_info.save()
        return redirect(url_for('student_info.list'))

    return render_template('student_info_edit.html', student_info=student_info)