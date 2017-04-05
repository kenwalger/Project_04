import datetime

from peewee import *

db = SqliteDatabase('worklog.db')


class Task(Model):
    task_name = CharField()
    user_name = CharField()
    minutes = IntegerField()
    date = DateField(default=datetime.date.today)
    notes = TextField()

    class Meta:
        database = db
        db_table = 'task'


def initialize():
    """Create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Task], safe=True)


def save(task):
    """Save a task to the database"""
    return Task.create(task_name=task['task_name'],
                       user_name=task['user_name'],
                       minutes=task['minutes'], notes=task['notes'])


def delete(task):
    if input("\nConfirm delete task? (yN): ").lower().strip() == "y":
        task.delete_instance()

# Make sure the db exists on import
initialize()