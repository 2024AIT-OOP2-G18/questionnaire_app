from peewee import SqliteDatabase
from .db import db
from .user import User
from .product import Product
from .order import Order
from .commute import Commute
from .lunch import Lunch
from .parttimer import Parttimer
from .student_info import Student_info

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    User,
    Product,
    Order,
    Commute,
    Lunch,
    Parttimer,
    Student_info,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()