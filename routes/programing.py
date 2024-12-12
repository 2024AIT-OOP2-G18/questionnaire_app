from flask import Blueprint, render_template, request, redirect, url_for
from models import Programing

# Blueprintの作成
programing_bp = Blueprint('programing', __name__, url_prefix='/programing')


@programing_bp.route('/')
def list():
    programing = Programing.select()
    return render_template('programing_list.html', title='アンケート', items=programing)


@programing_bp.route('/add', methods=['GET', 'POST'])
def add():
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        # 学籍番号の取得
        print(request.form)
        user_id = request.form['user_id']
        like = request.form['like']
        language = request.form['language']
        Programing.create(user_id=user_id, like=like, language=language)
        return redirect(url_for('programing.list'))
    
    return render_template('programing_add.html')


@programing_bp.route('/edit/<int:programing_id>', methods=['GET', 'POST'])
def edit(programing_id):
   programing = Programing.get_or_none(Programing.id == programing_id)
   if not programing:
       return redirect(url_for('programing.list'))

   if request.method == 'POST':
       programing.user_id = request.form['user_id']
       programing.like = request.form['like']
       programing.language = request.form['language']
       programing.save()
       return redirect(url_for('programing.list'))

   return render_template('programing_edit.html', programing=programing)