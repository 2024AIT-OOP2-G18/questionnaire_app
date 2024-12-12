from flask import Blueprint, render_template, request, redirect, url_for
from models import Lunch
from peewee import fn

# Blueprintの作成
lunch_bp = Blueprint('lunch', __name__, url_prefix='/lunches')


@lunch_bp.route('/')
def list():
    lunches = Lunch.select()
    #集計
    lunch_counts = (
        Lunch.select(Lunch.lunch_place, fn.COUNT(Lunch.lunch_place).alias('count'))
        .group_by(Lunch.lunch_place)
        .order_by(-fn.COUNT(Lunch.lunch_place))
    )
    #合計
    total_count = sum(row.count for row in lunch_counts)
    #比率
    lunch_ratios = [
        {
            "lunch_place": row.lunch_place,
            "count": row.count,
            "ratio": (row.count / total_count * 100) if total_count > 0 else 0
        }
        for row in lunch_counts
    ]
    #グラフの要素
    labels = [row.lunch_place for row in lunch_counts]
    return render_template('lunch_list.html', title='昼食アンケート', items=lunches, lunch_counts=lunch_counts, labels=labels, lunch_ratios=lunch_ratios)



@lunch_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        number = request.form['number']
        lunch_place = request.form['lunch_place']
        Lunch.create(number=number, lunch_place=lunch_place)
        return redirect(url_for('lunch.list'))
    
    return render_template('lunch_add.html')


@lunch_bp.route('/edit/<int:lunch_id>', methods=['GET', 'POST'])
def edit(lunch_id):
    lunch = Lunch.get_or_none(Lunch.id == lunch_id)
    if not lunch:
        return redirect(url_for('lunch.list'))

    if request.method == 'POST':
        lunch.number = request.form['number']
        lunch.lunch_place = request.form['lunch_place']
        lunch.save()
        return redirect(url_for('lunch.list'))

    return render_template('lunch_edit.html', lunch=lunch)