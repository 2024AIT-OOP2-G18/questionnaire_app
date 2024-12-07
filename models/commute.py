from peewee import Model ,CharField , IntegerField
from .db import db

class Commute(Model):
    way = CharField()
    time = IntegerField()

    class Meta:
        database = db