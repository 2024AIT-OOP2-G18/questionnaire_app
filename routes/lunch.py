from flask import Blueprint, render_template, request, redirect, url_for
from models import Lunch

# Blueprintの作成
lunch_bp = Blueprint('lunch', __name__, url_prefix='/lunches')


@lunch_bp.route('/')
def list():
    lunches = Lunch.select()
    return render_template('lunch_list.html', title='昼食アンケート', items=lunches)


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