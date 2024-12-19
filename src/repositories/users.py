import bcrypt
import psycopg2
from ..settings import DB_CONFIG

def create_user(role_id, username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = """
        INSERT INTO users (role_id, username, email, password, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        RETURNING id
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (role_id, username, email, hashed_password))
    conn.commit()

    user_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return user_id

def get_user(user_id):
    query = """
        SELECT id, role_id, username, email, created_at
        FROM users
        WHERE id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_id(user_id):
    query = """
        SELECT id, username, email, role_id, created_at
        FROM users
        WHERE id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role_id": user[3],
            "created_at": user[4]
        }
    else:
        return None
def get_all_users():
    query = """
        SELECT id, username FROM users
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Преобразуем кортежи в словари
    return [{"id": user[0], "username": user[1]} for user in users]

def get_user_role(user_id):
    # Подключаемся к базе данных
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # Запрос для получения роли пользователя по его user_id
        cursor.execute("""
            SELECT roles.name
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.id = %s
        """, (user_id,))

        # Извлекаем результат
        result = cursor.fetchone()

        if result:
            return result[0]  # Возвращаем название роли
        else:
            return None  # Если пользователь не найден

    except Exception as e:
        print(f"Error fetching user role: {e}")
        return None

    finally:
        cursor.close()
        conn.close()