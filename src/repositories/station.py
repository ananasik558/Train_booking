import psycopg2
from ..settings import DB_CONFIG

def get_all_stations():
    query = """
        SELECT id, name
        FROM station
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    stations = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [{"id": station[0], "name": station[1]} for station in stations]
