from peewee import *
import time
import json
from playhouse.migrate import *


conn = SqliteDatabase('database.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0}
    )
migrator = SqliteMigrator(conn)


class BaseModel(Model):
    class Meta:
        database = conn


class User(BaseModel):
    id = AutoField(column_name='id')
    chat_id = BigIntegerField(column_name='chat_id')
    user_id = BigIntegerField(column_name='user_id')
    username = TextField(column_name='username', default='Нет')

    warns = IntegerField(column_name='warns', default=0)
    mute = BigIntegerField(column_name='mute', default=0)
    banned = BooleanField(column_name='banned', default=False)

    moderator = BooleanField(column_name='moderator', default=False)

    class Meta:
        table_name = 'users'


class BadWords(BaseModel):
    word = TextField(column_name='word', null=False)

    class Meta:
        table_name = 'bad_words'


class Alerts(BaseModel):
    message_id = BigIntegerField(column_name='message_id', default=0)
    from_chat_id = BigIntegerField(column_name='from_chat_id', default=0)
    chat_id = BigIntegerField(column_name='chat_id', default=0)
    time = TextField(column_name='time', default=0)
    alerted = BooleanField(column_name='alerted', default=False)
    loop = BooleanField(column_name='loop', default=False)

    class Meta:
        table_name = 'alerts'


conn.connect()

User.create_table()
BadWords.create_table()
Alerts.create_table()

cursor = conn.cursor()

conn.close()