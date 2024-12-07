from peewee import Model, CharField
from .db import db

class Lunch(Model):
    number = CharField()
    lunch_place = CharField()

    class Meta:
        database = db