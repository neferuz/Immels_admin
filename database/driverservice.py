from sqlalchemy import desc, extract
from .models import User, Driver
from datetime import datetime, timedelta
from database import get_db1, get_db2
from sqlalchemy.sql import func, and_


# Удаление водителя по ID
def delete_driver_db(driver_id: int):
    db = next(get_db2())
    driver = db.query(Driver).filter_by(id=driver_id).first()
    if driver:
        db.delete(driver)
        db.commit()
        return True
    return False


# Просмотр списка всех водителей
def get_all_drivers_db():
    db = next(get_db2())
    drivers = db.query(Driver).all()
    return drivers


# Просмотр детальной информации о водителе по ID
def get_detailed_driver_db(driver_id: int):
    db = next(get_db2())
    driver = db.query(Driver).filter_by(id=driver_id).first()
    if driver:
        return driver
    return None


# Поиск водителей по строковому запросу
def search_driver_db(query: str):
    db = next(get_db2())
    drivers = db.query(Driver).filter(
        (Driver.name.like(f"%{query}%")) |
        (Driver.surname.like(f"%{query}%")) |
        (Driver.middle_name.like(f"%{query}%")) |
        (Driver.phone_number.like(f"%{query}%")) |
        (Driver.car_plate.like(f"%{query}%")) |
        (Driver.license_number.like(f"%{query}%"))
    ).all()
    return drivers


# Получение статистики по водителям
def get_statistics_db():
    db = next(get_db2())

    # Получаем общее количество водителей
    total_drivers = db.query(func.count(Driver.id)).scalar()

    # Получаем количество водителей за вчерашний день
    yesterday_drivers = get_yesterday_driver_count()

    # Рассчитываем процент роста
    if yesterday_drivers == 0:
        growth_percentage = 100.0
    else:
        growth_percentage = ((total_drivers - yesterday_drivers) / yesterday_drivers) * 100

    return {
        "total_drivers": total_drivers,
        "growth_percentage": growth_percentage
    }


# Получение количества водителей за вчерашний день
def get_yesterday_driver_count():
    db = next(get_db2())
    yesterday_users = db.query(func.count(Driver.id)).filter(User.created_at < func.now() - timedelta(days=1)).scalar()
    return yesterday_users


# Получение общего количества водителей
def get_drivers_count_db():
    db = next(get_db2())
    return db.query(func.count(Driver.id)).scalar()


# Регистрация нового водителя
def register_driver_db(
        name: str,
        surname: str,
        middle_name: str,
        phone_number: str,
        age: int,
        gender: str,
        rating: float,
        license_number: str,
        car_plate: str,
        car_model: str,
        status: str,
        tariff_id: int
):
    db = next(get_db2())
    existing_driver = db.query(Driver).filter_by(phone_number=phone_number).first()
    if existing_driver:
        return "Driver with this phone number already exists"

    existing_driver = db.query(Driver).filter_by(license_number=license_number).first()
    if existing_driver:
        return "Driver with this license number already exists"

    existing_driver = db.query(Driver).filter_by(car_plate=car_plate).first()
    if existing_driver:
        return "Driver with this car plate already exists"

    new_driver = Driver(
        name=name,
        surname=surname,
        middle_name=middle_name,
        phone_number=phone_number,
        age=age,
        car_plate=car_plate,
        car_model=car_model,
        gender=gender,
        rating=rating,
        license_number=license_number,
        status=status,
        tariff_id=tariff_id,
        created_at=datetime.now()
    )

    db.add(new_driver)
    db.commit()
    return 'Driver successfully registered'


# Получение топ-3 водителей по рейтингу
def get_top_three_drivers_db():
    db = next(get_db2())
    return db.query(Driver).order_by(desc(Driver.rating)).limit(3).all()


# Подсчет количества водителей, зарегистрированных в указанном месяце
# Подсчет количества пользователей, зарегистрированных за последние 7 месяцев
def count_drivers_registered_in_last_7_months_db() -> int:
    db = next(get_db2())
    now = datetime.now()
    start_date = now - timedelta(days=30 * 7)  # грубое приближение 7 месяцев назад

    count = db.query(func.count(Driver.id)).filter(
        and_(
            Driver.created_at >= start_date,
            Driver.created_at <= now
        )
    ).scalar()
    return count
