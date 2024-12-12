from flask import Blueprint, render_template, request, redirect, url_for
from models import PartTimer
from peewee import fn

# Blueprintの作成
parttimer_bp = Blueprint('parttimer', __name__, url_prefix='/parttimers')


@parttimer_bp.route('/')
def list():
    parttimers = PartTimer.select()
    return render_template('parttimer_list.html', title='アルバイトに関するアンケート', items=parttimers)


@parttimer_bp.route('/add', methods=['GET', 'POST'])
def add():

    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        hourlypay = request.form['hourlypay']
        PartTimer.create(name=name, category=category, hourlypay=hourlypay)
        return redirect(url_for('parttimer.list'))

    return render_template('parttimer_add.html')


@parttimer_bp.route('/edit/<int:parttimer_id>', methods=['GET', 'POST'])
def edit(parttimer_id):
    parttimer = PartTimer.get_or_none(PartTimer.id == parttimer_id)
    if not parttimer:
        return redirect(url_for('parttimer.list'))

    if request.method == 'POST':
        parttimer.name = request.form['name']
        parttimer.category = request.form['category']
        parttimer.hourlypay = request.form['hourlypay']
        parttimer.save()
        return redirect(url_for('parttimer.list'))

    return render_template('parttimer_edit.html', parttimer=parttimer)


@parttimer_bp.route('/stats')
def stats():
    # カテゴリー別人数の集計
    category_data = (
        PartTimer
        .select(PartTimer.category, fn.COUNT(PartTimer.id).alias('count'))
        .group_by(PartTimer.category)
    )
    category_labels = [row.category for row in category_data]
    category_values = [row.count for row in category_data]

    # 時給の統計値計算
    hourlypay_stats = PartTimer.select(
        fn.MIN(PartTimer.hourlypay).alias('min'),
        fn.MAX(PartTimer.hourlypay).alias('max'),
        fn.AVG(PartTimer.hourlypay).alias('avg')
    ).dicts().get()

     # 平均時給のフォーマット
    hourlypay_stats['avg'] = round(hourlypay_stats['avg'], 2) if hourlypay_stats['avg'] is not None else None

    return render_template(
        'parttimer_stats.html',
        category_data={"labels": category_labels, "values": category_values},
        hourlypay_stats=hourlypay_stats
    )