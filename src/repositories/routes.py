import psycopg2
from ..settings import DB_CONFIG

def create_route(train_id, start_station, finish_station):
    try:
        # Открываем соединение с базой данных
        connection = psycopg2.connect(**DB_CONFIG)

        # Подготовка запроса для вставки данных
        query = """
            INSERT INTO routes (train_id, start_station, finish_station)
            VALUES (%s, %s, %s) RETURNING id;
        """
        cursor = connection.cursor()
        
        # Выполнение запроса
        print(f"Executing query: {query} with values: ({train_id}, {start_station}, {finish_station})")
        cursor.execute(query, (train_id, start_station, finish_station))

        # Получаем ID маршрута
        route_id = cursor.fetchone()
        
        if route_id:
            route_id = route_id[0]  # Извлекаем ID маршрута из результата
            print(f"Route created successfully with ID {route_id}")
        else:
            print("Failed to create route: No ID returned.")

        connection.commit()
        cursor.close()
        connection.close()  # Закрываем соединение после выполнения
        return route_id
    except Exception as e:
        print(f"Error creating route: {e}")
        return None


def get_route_by_id(route_id):
    query = """
        SELECT r.id, r.train_id, r.start_station, r.finish_station, t.type, s1.name AS start_station_name, s2.name AS finish_station_name
        FROM routes r
        JOIN trains t ON r.train_id = t.id
        JOIN station s1 ON r.start_station = s1.id
        JOIN station s2 ON r.finish_station = s2.id
        WHERE r.id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (route_id,))
    route = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if route:
        return {
            "id": route[0],
            "train_id": route[1],
            "start_station": route[2],
            "finish_station": route[3],
            "train_type": route[4],
            "start_station_name": route[5],
            "finish_station_name": route[6]
        }
    else:
        return None

def get_routes_by_train(train_id):
    query = """
        SELECT r.id, r.start_station, r.finish_station, s1.name AS start_station_name, s2.name AS finish_station_name
        FROM routes r
        JOIN station s1 ON r.start_station = s1.id
        JOIN station s2 ON r.finish_station = s2.id
        WHERE r.train_id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (train_id,))
    routes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {"id": r[0], "start_station": r[1], "finish_station": r[2], "start_station_name": r[3], "finish_station_name": r[4]}
        for r in routes
    ]

def get_routes_by_station(station_id):
    query = """
        SELECT r.id, r.train_id, t.type, s1.name AS start_station_name, s2.name AS finish_station_name
        FROM routes r
        JOIN trains t ON r.train_id = t.id
        JOIN station s1 ON r.start_station = s1.id
        JOIN station s2 ON r.finish_station = s2.id
        WHERE r.start_station = %s OR r.finish_station = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (station_id, station_id))
    routes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {"id": r[0], "train_id": r[1], "train_type": r[2], "start_station_name": r[3], "finish_station_name": r[4]}
        for r in routes
    ]

def get_all_routes():
    query = """
        SELECT r.id, r.train_id, r.start_station, r.finish_station, t.type, s1.name AS start_station_name, s2.name AS finish_station_name
        FROM routes r
        JOIN trains t ON r.train_id = t.id
        JOIN station s1 ON r.start_station = s1.id
        JOIN station s2 ON r.finish_station = s2.id
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    routes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {"id": r[0], "train_id": r[1], "start_station": r[2], "finish_station": r[3], "train_type": r[4], "start_station_name": r[5], "finish_station_name": r[6]}
        for r in routes
    ]
