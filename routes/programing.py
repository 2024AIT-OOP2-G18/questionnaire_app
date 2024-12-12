from flask import Blueprint, render_template, request, redirect, url_for
from models import Programing
from collections import Counter

# Blueprintの作成
programing_bp = Blueprint('programing', __name__, url_prefix='/programing')


@programing_bp.route('/')
def list():
    programing = Programing.select()

        # like の統計
    like_counter = Counter([item.like for item in programing])
    total_likes = sum(like_counter.values())
    like_stats = {key: (value / total_likes) * 100 for key, value in like_counter.items()}  # パーセンテージ計算

    # language の統計
    language_counter = Counter([item.language for item in programing])
    total_languages = sum(language_counter.values())
    language_stats = {key: (value / total_languages) * 100 for key, value in language_counter.items()}  # パーセンテージ計算

    return render_template('programing_list.html', 
                           title='アンケート',
                            items=programing,
                            like_stats=like_stats,
                            language_stats=language_stats
                            )


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


#@programing_bp.route('/edit/<int:progrmaing_id>', methods=['GET', 'POST'])
#def edit(programing_id):
#    programing = Programing.get_or_none(Programing.id == programing_id)
#    if not programing:
#        return redirect(url_for('programing.list'))
#
#    if request.method == 'POST':
#        programing.name = request.form['name']
#        programing.like = request.form['like']
#        programing.language = request.form['language']
#        programing.save()
#        return redirect(url_for('programing.list'))
#
#    return render_template('programing_edit.html', programing=programing)
