from peewee import Model, CharField, IntegerField, ForeignKeyField
from .db import db

class Student_info(Model):
    id = CharField()
    name = CharField()
    sex = CharField()
    age = IntegerField()

    class Meta:
        database = db