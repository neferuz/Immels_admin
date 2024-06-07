from .models import User, Tariff, Order
from datetime import datetime
from database import get_db1, get_db2


# Добавление нового тарифа
def add_tariff_db(
        name: str,
):
    db = next(get_db2())

    existing_tariff = db.query(Tariff).filter_by(name=name).first()
    if existing_tariff:
        return "Tariff with this name already exists"

    new_tariff = Tariff(name=name, created_at=datetime.now())

    db.add(new_tariff)
    db.commit()
    return 'Tariff successfully added'


# Получение списка всех тарифов
def get_all_tariffs_db():
    db = next(get_db2())
    tariffs = db.query(Tariff).all()
    return tariffs


# Получение детальной информации о тарифе по ID
def get_detailed_tariff_db(tariff_id: int):
    db = next(get_db2())
    tariff = db.query(Tariff).filter_by(id=tariff_id).first()
    return tariff


# Поиск тарифов по строковому запросу
def search_tariff_db(query: str):
    db = next(get_db2())
    tariff = db.query(Tariff).filter(Tariff.name.like(f"%{query}%")).all()
    return tariff


# Получение всех заказов для указанного тарифа по его ID
def get_orders_of_this_tariff_db(tariff_id: int):
    db = next(get_db2())
    orders = db.query(Order).filter_by(tariff_id=tariff_id).all()
    return orders
