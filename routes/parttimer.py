from flask import Blueprint, render_template, request, redirect, url_for
from models import Parttimer

# Blueprintの作成
parttimer_bp = Blueprint('parttimer', __name__, url_prefix='/parttime')

@parttimer_bp.route('/')
def list():
    parttimer = Parttimer.select()
    return render_template('parttimer_list.html', title='アルバイト', items=parttimer)


@parttimer_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        hourlypay = request.form['hourlypay']
        Parttimer.create(name=name, category=category, hourlypay=hourlypay)
        return redirect(url_for('parttimer.list'))
    
    return render_template('parttimer_add.html')


@parttimer_bp.route('/edit/<int:parttimer_id>', methods=['GET', 'POST'])
def edit(parttimer_id):
    parttimer = Parttimer.get_or_none(Parttimer.id == parttimer_id)
    if not parttimer:
        return redirect(url_for('parttimer.list'))

    if request.method == 'POST':
        parttimer.name = request.form['name']
        parttimer.category = request.form['category']
        parttimer.hourlypay = request.form['hourlypay']
        parttimer.save()
        return redirect(url_for('parttimer.list'))

    return render_template('parttimer_edit.html', parttimer=parttimer)