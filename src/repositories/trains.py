import psycopg2
from psycopg2.extras import RealDictCursor
from src.settings import DB_CONFIG  # Предполагается, что DB_CONFIG содержит настройки подключения

# Создание записи о новом поезде
def create_train(train_type, start_time):
    query = """
        INSERT INTO trains (type, start_time)
        VALUES (%s, %s)
        RETURNING id
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (train_type, start_time))
        train_id = cursor.fetchone()[0]
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return train_id

# Удаление поезда по ID
def delete_train(train_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Удаляем доступные места, связанные с этим поездом
        query_delete_seats = "DELETE FROM available_seats WHERE train_id = %s;"
        cursor.execute(query_delete_seats, (train_id,))
        conn.commit()

        # Удаляем маршруты, связанные с этим поездом
        query_delete_routes = "DELETE FROM routes WHERE train_id = %s;"
        cursor.execute(query_delete_routes, (train_id,))
        conn.commit()

        # Удаляем билеты, связанные с этим поездом
        query_delete_tickets = "DELETE FROM tickets WHERE followed_train_id = %s;"
        cursor.execute(query_delete_tickets, (train_id,))
        conn.commit()

        # Теперь можно удалить сам поезд
        query_delete_train = "DELETE FROM trains WHERE id = %s;"
        cursor.execute(query_delete_train, (train_id,))
        conn.commit()

        print(f"Train {train_id}, its routes, available seats, and associated tickets deleted successfully.")
    except Exception as e:
        conn.rollback()  # В случае ошибки откатываем изменения
        print(f"Error deleting train and associated data: {e}")



# Получение информации о поезде по ID
def get_train_by_id(train_id):
    query = """
        SELECT id, type, start_time
        FROM trains
        WHERE id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, (train_id,))
        train = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    return train

# Получение всех поездов
def get_all_trains():
    query = """
        SELECT id, type, start_time
        FROM trains
        ORDER BY start_time ASC
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query)
        trains = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return trains

# Обновление информации о поезде
def update_train(train_id, train_type=None, start_time=None):
    query = "UPDATE trains SET"
    fields = []
    params = []

    if train_type is not None:
        fields.append("type = %s")
        params.append(train_type)
    if start_time is not None:
        fields.append("start_time = %s")
        params.append(start_time)

    if not fields:
        raise ValueError("Нет данных для обновления")

    query += ", ".join(fields) + " WHERE id = %s"
    params.append(train_id)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    finally:
        cursor.close()
        conn.close()
