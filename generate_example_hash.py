import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Примеры хэширования
passwords = {
    "superadmin": hash_password("superadmin"),
    "denis": hash_password("denis"),
    "tigran": hash_password("tigran"),
    "user_4": hash_password("user_4"),
    "user_5": hash_password("user_5"),
    "user_6": hash_password("user_6")
}

# Выводим хэши для использования в SQL
for username, hashed_password in passwords.items():
    print(f"{hashed_password}")