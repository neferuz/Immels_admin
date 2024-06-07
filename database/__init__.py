from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Подключение к базе данных 1
SQLALCHEMY_DATABASE_URL1 = 'postgresql://postgres:1234@localhost/imells'
engine1 = create_engine(SQLALCHEMY_DATABASE_URL1, pool_size=20, max_overflow=10)
SessionLocal1 = sessionmaker(bind=engine1)

# Подключение к базе данных 2
SQLALCHEMY_DATABASE_URL2 = 'postgresql://postgres:1234@localhost/imells_admin'
engine2 = create_engine(SQLALCHEMY_DATABASE_URL2, pool_size=20, max_overflow=10)
SessionLocal2 = sessionmaker(bind=engine2)

# Создание базового класса
Base = declarative_base()


# Создание сессий
def get_db1():
    db = SessionLocal1()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db2():
    db = SessionLocal2()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
