import streamlit as st
from ..repositories.trains import create_train, delete_train, get_all_trains
from ..repositories.users import get_user_role 

def show_trains_page():
    st.title("Manage Trains")
    user_id = st.session_state.get('user_id')
    user_role = get_user_role(user_id)
    # Проверка, есть ли в сессии информация о пользователе и его роли
    if user_role != "admin":
        st.error("Only admin can create routes.")
        return
    # Боковое меню
    menu_option = st.sidebar.radio(
        "Select an action",
        ["Add a Train", "Delete a Train", "View All Trains"]
    )

    # "Add a Train"
    if menu_option == "Add a Train":
        st.subheader("Add a New Train")
        
        # Ввод данных для нового поезда
        train_type = st.text_input("Enter Train Type:")
        start_time = st.date_input("Select Start Date:")
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")  # Преобразуем дату в строку

        if st.button("Add Train"):
            try:
                train_id = create_train(train_type, start_time)
                if train_id:
                    st.success(f"Train added successfully with ID {train_id}.")
            except Exception as e:
                st.error(f"Failed to add train: {e}")

    # "Delete a Train"
    elif menu_option == "Delete a Train":
        st.subheader("Delete a Train")

        # Получаем список всех поездов
        trains = get_all_trains()  # Функция для получения всех поездов

        if trains:
            train_options = {f"Train ID: {train['id']} - Type: {train['type']}": train['id'] for train in trains}
            selected_train = st.selectbox("Select a train to delete:", list(train_options.keys()))

            if st.button("Delete Train"):
                try:
                    delete_train(train_options[selected_train])
                    st.success(f"Train {selected_train} has been deleted.")
                except Exception as e:
                    st.error(f"Failed to delete train: {e}")
        else:
            st.warning("No trains available to delete.")

    # "View All Trains"
    elif menu_option == "View All Trains":
        st.subheader("View All Trains")
        
        trains = get_all_trains()
        if trains:
            for train in trains:
                st.write(f"**Train ID**: {train['id']} - Type: {train['type']} - Start Time: {train['start_time']}")
        else:
            st.info("No trains found.")
