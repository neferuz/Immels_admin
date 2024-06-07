from fastapi import APIRouter, HTTPException
from database.userservice import *

users_router = APIRouter(tags=['Управление пользователями'], prefix='/users')


# Удаление пользователя
@users_router.delete("/api/delete_user", response_model=bool)
async def delete_user(user_id: int):
    result = delete_user_db(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return True


# Получение списка всех пользователей
@users_router.get("/api/get_all_users")
async def get_all_users():
    return get_all_users_db()


# Получение детальной информации о пользователе
@users_router.get("/api/get_detailed_user/{user_id}")
async def get_detailed_user(user_id: int):
    user = get_detailed_user_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Поиск пользователей
@users_router.get("/api/search_user")
async def search_user(query: str):
    return search_user_db(query)


# Получение статистики по пользователям
@users_router.get("/api/user_statistics")
async def get_statistics():
    return get_statistics_db()


# Получение количества пользователей
@users_router.get('/api/get_users_count')
async def get_users_count():
    return get_users_count_db()


# Подсчет количества зарегистрированных пользователей за последние 7 месяцев
@users_router.get('/api/count_users_registered_in_last_7_months')
async def count_users_registered_in_last_7_months():
    count = count_users_registered_in_last_7_months_db()
    return {"count": count}
