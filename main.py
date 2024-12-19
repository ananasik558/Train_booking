import streamlit as st
from src.pages.auth_page import show_login_page
from src.pages.route_page import show_routes_page
from src.pages.ticket_page import show_tickets_page
from src.pages.train_page import show_trains_page

# Хранилище для текущего пользователя и его роли
if "role_id" not in st.session_state:
    st.session_state["role_id"] = None  # Роль пользователя
    st.session_state["use_name"] = None  # Имя пользователя

def main():
    st.sidebar.title("Navigation")

    # Если пользователь еще не вошел, показываем только страницу аутентификации
    if not st.session_state.get("role_id"):
        st.sidebar.write("Please log in to access the application.")
        show_login_page()
        return

    # Получаем role_id и определяем роль
    role_id = st.session_state.get('role_id', None)

    # Определяем роль пользователя
    role_name = "Admin" if role_id == 1 else None

    # Выводим информацию о пользователе в сайдбаре
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if role_name:
        st.sidebar.write(f"Role: {role_name}")

    # Навигация по страницам
    pages = {
        "Tickets": show_tickets_page,
        "Routes": show_routes_page,
        "Train": show_trains_page,
    }

    # Роли и доступные страницы
    role_permissions = {
         1: list(pages.keys()),  # Админ видит все страницы
         2: list(pages.keys()),  # Юзер видит все страницы (логику ограничений можно реализовать внутри страниц)
    }

    # Получаем доступные страницы для текущей роли
    available_pages = role_permissions.get(st.session_state["role_id"], [])

    # Выбор страницы
    page = st.sidebar.selectbox("Go to", available_pages)

    # Переход на выбранную страницу
    if page in pages:
        pages[page]()


if __name__ == "__main__":
    main()