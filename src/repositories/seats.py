import psycopg2
from ..settings import DB_CONFIG

def get_all_available_seats():
    query = """
        SELECT id, train_id, seat_number, status
        FROM available_seats
        WHERE status = 'available'
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    available_seats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {"id": seat[0], "train_id": seat[1], "seat_number": seat[2], "status": seat[3]}
        for seat in available_seats
    ]

def get_available_seats_by_train(train_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        query = "SELECT id, seat_number, status FROM available_seats WHERE train_id = %s AND status = 'available';"
        cursor.execute(query, (train_id,))
        seats = cursor.fetchall()
        cursor.close()
        conn.close()
        # Преобразуем результат в список словарей
        return [{"id": seat[0], "seat_number": seat[1], "status": seat[2]} for seat in seats]
    except Exception as e:
        print(f"Error fetching seats for train {train_id}: {e}")
        return []
