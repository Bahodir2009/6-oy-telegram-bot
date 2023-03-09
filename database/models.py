from peewee import *
from data.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT

db = PostgresqlDatabase(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
# db = SqliteDatabase('peewee_bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigIntegerField(primary_key=True, unique=True)
    username = CharField(max_length=100)
    date = DateTimeField(formats=['%Y-%m-%d %H:%M'])

    class Meta:
        db_name = 'users'


class Effects(BaseModel):
    effect_name = CharField(max_length=50)
    effect = CharField(max_length=50)

    class Meta:
        db_name = 'effects'

