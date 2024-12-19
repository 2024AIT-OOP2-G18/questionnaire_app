from flask import Blueprint, render_template, request, redirect, url_for
from models import  Commute

# Blueprintの作成
commute_bp = Blueprint('commute', __name__, url_prefix='/commutes')

@commute_bp.route('/')
def list():
    commutes = Commute.select()
    count = Commute.select().count()

    data = [[0, 0], [0, 0], [0, 0]]

    #データ読み込み
    for element in commutes:
        if element.way == "徒歩":
            data[0][0] += 1             #徒歩の合計人数
            data[0][1] += element.time  #徒歩の合計通学時間
        if element.way == "車":
            data[1][0] += 1             #車の合計人数
            data[1][1] += element.time  #車の合計通学時間
        if element.way == "公共交通機関":
            data[2][0] += 1             #公共交通機関の合計人数
            data[2][1] += element.time  #公共交通機関の合計通学時間

    average = [0, 0, 0]

    #平均値計算(０で割るとエラー吐くから排他処理)
    if(data[0][0] != 0):
        average[0] = data[0][1] / data[0][0]    #徒歩の平均時間
    if(data[1][0] != 0):
        average[1] = data[1][1] / data[1][0]    #車の平均時間
    if(data[2][0] != 0):
        average[2] = data[2][1] / data[2][0]    #公共交通機関の平均時間

    rate = [0, 0, 0]
    if(count != 0):
        rate[0] = data[0][0] / count * 100
        rate[1] = data[1][0] / count * 100
        rate[2] = data[2][0] / count * 100

    return render_template('commute_list.html', title='通学情報一覧', items=commutes, data = data, average = average,rate = rate)

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
