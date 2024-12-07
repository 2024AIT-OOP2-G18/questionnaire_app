from peewee import Model, CharField, DecimalField
from .db import db

class Parttimer(Model):
    name = CharField()
    category = CharField()
    hourlypay = DecimalField()

    class Meta:
        database = db