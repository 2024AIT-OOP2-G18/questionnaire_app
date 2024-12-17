from peewee import Model, CharField, IntegerField
from .db import db

class PartTimer(Model):
    name = CharField()
    category = IntegerField()
    hourlypay = IntegerField()

    class Meta:
        database = db