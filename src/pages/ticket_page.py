import streamlit as st
from ..repositories.ticket import create_ticket, delete_ticket, get_tickets_by_user
from ..repositories.users import get_all_users, get_user_by_id
from ..repositories.trains import get_all_trains
from ..repositories.seats import get_all_available_seats


def show_tickets_page():
    st.title("Manage Tickets")

    # Проверка авторизации
    if "user_id" not in st.session_state:
        st.warning("Please log in to manage tickets.")
        return

    current_user_id = st.session_state["user_id"]

    # Добавим кнопку для разлогинивания
    if st.button("Log out"):
        # Очищаем данные сессии
        del st.session_state["user_id"]
        st.success("You have been logged out.")
        return  # Прерываем выполнение функции, так как пользователь разлогинился

    # Боковое меню
    menu_option = st.sidebar.radio(
        "Select an action",
        ["Buy a Ticket", "Cancel a Ticket", "Your Tickets"]
    )

    # "Buy a Ticket"
    if menu_option == "Buy a Ticket":
        st.subheader("Buy a Ticket")

        try:
            # Получаем все поезда и доступные места
            trains = get_all_trains()  # Функция для получения всех поездов
            available_seats = get_all_available_seats()  # Функция для получения всех доступных мест

            if trains and available_seats:
                # Селектор для выбора поезда и места
                selected_train = st.selectbox(
                    "Select a train:",
                    options=trains,
                    format_func=lambda train: f"Train ID: {train['id']} - Type: {train['type']}"
                )

                selected_seat = st.selectbox(
                    "Select a seat:",
                    options=available_seats,
                    format_func=lambda seat: f"Seat Number: {seat['seat_number']} - Status: {seat['status']}"
                )

                if st.button("Buy Ticket"):
                    try:
                        create_ticket(current_user_id, selected_train["id"], selected_seat["id"])
                        st.success(f"You have successfully bought a ticket for Train {selected_train['id']}, Seat {selected_seat['seat_number']}.")
                    except Exception as e:
                        st.error(f"Failed to buy ticket: {e}")
            else:
                st.write("No trains or available seats.")
        except Exception as e:
            st.error(f"Failed to load trains or seats: {e}")

    # "Cancel a Ticket"
    elif menu_option == "Cancel a Ticket":
        st.subheader("Cancel a Ticket")

        try:
            # Получаем список билетов текущего пользователя
            tickets = get_tickets_by_user(current_user_id)

            if tickets:
                # Селектор для выбора билета
                selected_ticket = st.selectbox(
                    "Select a ticket to cancel:",
                    options=tickets,
                    format_func=lambda ticket: f"Train ID: {ticket[1]} - Seat: {ticket[2]}"
                )

                if st.button("Cancel Ticket"):
                    try:
                        delete_ticket(selected_ticket[0])
                        st.success(f"You have successfully canceled the ticket for Train {selected_ticket[1]}, Seat {selected_ticket[2]}.")
                    except Exception as e:
                        st.error(f"Failed to cancel ticket: {e}")
            else:
                st.write("You have no tickets to cancel.")
        except Exception as e:
            st.error(f"Failed to load your tickets: {e}")

    # "Your Tickets"
    # Обработчик для отображения билетов пользователя
    elif menu_option == "Your Tickets":
        st.subheader("Your Tickets")

        try:
            tickets = get_tickets_by_user(current_user_id)
            if tickets:
                st.write("You have the following tickets:")
                for ticket in tickets:
                    st.write(f"Ticket ID: {ticket[0]} - Train ID: {ticket[1]} - Seat ID: {ticket[2]} - Created At: {ticket[3]}")
            else:
                st.write("You have no tickets.")
        except Exception as e:
            st.error(f"Failed to fetch your tickets: {e}")

