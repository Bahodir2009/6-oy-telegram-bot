import datetime

from playhouse.shortcuts import model_to_dict

from data.config import ADMINS
from .models import *


async def add_user(user_id: int, username: str, date: datetime):
    with db:
        if not Users.select().where(Users.user_id == user_id).exists():
            Users.create(user_id=user_id, username=username, date=date)


async def get_all_effects():
    with db:
        effects = Effects.select()
        effects = [model_to_dict(item) for item in effects]
        return effects


async def get_users_info():
    with db:
        users = Users.select(Users.date)
        users_date = [model_to_dict(item) for item in users]
        total_users = users.count()
        return users_date, total_users


async def get_effect(text):
    with db:
        return [model_to_dict(item) for item in Effects.select(Effects.effect).where(Effects.effect_name == text)]

