import psycopg2
from ..settings import DB_CONFIG

def create_ticket(following_user_id, followed_train_id, followed_seat_id):
    # Запрос для вставки билета и обновления статуса места
    query = """
        WITH updated_seat AS (
            UPDATE available_seats
            SET status = 'occupied'
            WHERE id = %s
            RETURNING train_id, seat_number, status
        )
        INSERT INTO tickets (following_user_id, followed_train_id, followed_seat_id, created_at)
        VALUES (%s, %s, %s, NOW());
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute(query, (followed_seat_id, following_user_id, followed_train_id, followed_seat_id))
    conn.commit()

    cursor.close()
    conn.close()

def delete_ticket(ticket_id):
    # Запрос для удаления билета и восстановления статуса места
    query = """
        WITH restored_seat AS (
            DELETE FROM tickets
            WHERE id = %s
            RETURNING followed_seat_id
        )
        UPDATE available_seats
        SET status = 'available'
        WHERE id = (SELECT followed_seat_id FROM restored_seat);
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (ticket_id,))
    conn.commit()

    cursor.close()
    conn.close()

def get_tickets_by_user(user_id):
    query = """
        SELECT t.id, t.followed_train_id, t.followed_seat_id, t.created_at
        FROM tickets t
        WHERE t.following_user_id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    tickets = cursor.fetchall()
    cursor.close()
    conn.close()
    return tickets


def get_users_by_ticket(ticket_id):
    query = """
        SELECT u.id, u.username
        FROM tickets t
        JOIN users u ON t.following_user_id = u.id
        WHERE t.id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (ticket_id,))
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": user[0], "username": user[1]} for user in users]

