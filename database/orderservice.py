from .models import Order
from datetime import datetime, timedelta
from database import get_db1, get_db2
from sqlalchemy.sql import func


# Создание нового заказа
def make_order_db(
        user_id: int,
        driver_id: int,
        tariff_id: int,
        start_location: str,
        end_location: str,
        distance: float,
        price: float
):
    db = next(get_db2())
    new_order = Order(
        user_id=user_id,
        driver_id=driver_id,
        tariff_id=tariff_id,
        start_location=start_location,
        end_location=end_location,
        distance=distance,
        price=price,
        created_at=datetime.now()
    )

    db.add(new_order)
    db.commit()
    return 'Order accepted!'


# Получение списка всех заказов
def get_all_orders_db():
    db = next(get_db2())
    orders = db.query(Order).all()
    return orders


# Получение детальной информации о заказе по ID
def get_detailed_order_db(order_id: int):
    db = next(get_db2())
    order = db.query(Order).filter_by(id=order_id).first()
    return order


# Поиск заказов по строковому запросу
def search_order_db(query: str):
    db = next(get_db2())
    orders = db.query(Order).filter(
        (Order.start_location.like(f"%{query}%")) |
        (Order.end_location.like(f"%{query}%")) |
        (Order.price.like(f"%{query}%"))
    ).all()
    return orders


# Получение общего количества заказов
def get_all_orders_count_db():
    db = next(get_db2())
    return db.query(func.count(Order.id)).scalar()


# Получение статистики по заказам
def get_statistics_db():
    db = next(get_db1())

    # Получаем общее количество заказов
    total_orders = db.query(func.count(Order.id)).scalar()

    # Получаем количество заказов за вчерашний день
    yesterday_orders = get_yesterday_order_count()

    # Рассчитываем процент роста
    if yesterday_orders == 0:
        growth_percentage = 100.0
    else:
        growth_percentage = ((total_orders - yesterday_orders) / yesterday_orders) * 100

    return {
        "total_orders": total_orders,
        "growth_percentage": growth_percentage
    }


# Получение количества заказов за вчерашний день
def get_yesterday_order_count():
    db = next(get_db1())
    yesterday_orders = db.query(func.count(Order.id)).filter(Order.created_at < func.now() - timedelta(days=1)).scalar()
    return yesterday_orders




