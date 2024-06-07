from sqlalchemy import extract
from .models import User, Order
from datetime import datetime, timedelta
from database import get_db1, get_db2
from sqlalchemy.sql import func, and_


# Удаление пользователя по ID
def delete_user_db(user_id: int):
    db = next(get_db1())
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# Просмотр списка всех пользователей
def get_all_users_db():
    db = next(get_db1())
    users = db.query(User).all()
    return users


# Просмотр детальной информации о пользователе по ID
def get_detailed_user_db(user_id: int):
    db = next(get_db1())
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        return user
    return None


# Поиск пользователей по строковому запросу
def search_user_db(query: str):
    db = next(get_db1())
    users = db.query(User).filter(
        (User.username.like(f"%{query}%")) |
        (User.fio.like(f"%{query}%")) |
        (User.phone_number.like(f"%{query}%"))
    ).all()
    return users


# Получение статистики по пользователям
def get_statistics_db():
    db = next(get_db1())

    # Получаем общее количество пользователей
    total_users = db.query(func.count(User.id)).scalar()

    # Получаем количество пользователей за вчерашний день
    yesterday_users = get_yesterday_user_count()

    # Рассчитываем процент роста
    if yesterday_users == 0:
        growth_percentage = 100.0
    else:
        growth_percentage = ((total_users - yesterday_users) / yesterday_users) * 100

    return {
        "total_users": total_users,
        "growth_percentage": growth_percentage
    }


# Получение количества пользователей за вчерашний день
def get_yesterday_user_count():
    db = next(get_db1())
    yesterday_users = db.query(func.count(User.id)).filter(User.created_at < func.now() - timedelta(days=1)).scalar()
    return yesterday_users


# Получение общего количества пользователей
def get_users_count_db():
    db = next(get_db1())
    return db.query(func.count(User.id)).scalar()


# Подсчет количества пользователей, зарегистрированных за последние 7 месяцев
def count_users_registered_in_last_7_months_db() -> int:
    db = next(get_db1())
    now = datetime.now()
    start_date = now - timedelta(days=30 * 7)  # грубое приближение 7 месяцев назад

    count = db.query(func.count(User.id)).filter(
        and_(
            User.created_at >= start_date,
            User.created_at <= now
        )
    ).scalar()
    return count
