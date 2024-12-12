from flask import Blueprint, render_template, request, redirect, url_for
from models import  Commute

# Blueprintの作成
commute_bp = Blueprint('commute', __name__, url_prefix='/commutes')


@commute_bp.route('/')
def list():
    commutes = Commute.select()
    return render_template('commute_list.html', title='通学情報一覧', items=commutes)


@commute_bp.route('/add', methods=['GET', 'POST'])
def add():
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        way = request.form['way']
        time = request.form['time']
        Commute.create(way=way,time=time)
        return redirect(url_for('commute.list'))

    return render_template('commute_add.html')


@commute_bp.route('/edit/<int:commute_id>', methods=['GET', 'POST'])
def edit(commute_id):
    commute = Commute.get_or_none(Commute.id == commute_id)
    if not commute:
        return redirect(url_for('commute.list'))

    if request.method == 'POST':
        commute.way = request.form['way']
        commute.time = request.form['time']
        commute.save()
        return redirect(url_for('commute.list'))

    return render_template('commute_edit.html', commute=commute)
