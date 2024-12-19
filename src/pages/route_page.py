import streamlit as st
from ..repositories.routes import create_route, get_route_by_id, get_routes_by_station, get_all_routes
from ..repositories.trains import get_all_trains
from ..repositories.station import get_all_stations
from ..repositories.users import get_user_role  # Функция для получения роли пользователя

# Главная функция страницы
def show_routes_page():
    st.title("Routes Management")

    # Получаем user_id из сессии
    user_id = st.session_state.get('user_id')  # Получаем user_id из сессии
    if not user_id:
        st.error("Please log in to access this page.")
        return

    # Получаем роль пользователя
    user_role = get_user_role(user_id)

    # Статичное меню слева с радиокнопками
    action = st.sidebar.radio(
        "Choose Action",
        [
            "Create New Route",
            "View Routes by Station",
            "View All Routes",
            "View Route Details",
        ],
    )

    # Разрешаем создание маршрута только для admin
    if action == "Create New Route":
        if user_role != "admin":
            st.error("Only admin can create routes.")
            return
        
        st.subheader("Create New Route")
        
        trains = get_all_trains()  # Получаем все поезда
        stations = get_all_stations()  # Получаем все станции

        train_names = {train["id"]: train["id"] for train in trains}
        start_station_names = {station["name"]: station["id"] for station in stations}
        finish_station_names = {station["name"]: station["id"] for station in stations}

        selected_train_name = st.selectbox("Select a train ID", list(train_names.keys()))
        selected_train_id = train_names[selected_train_name]

        selected_start_station_name = st.selectbox("Select a start station", list(start_station_names.keys()))
        selected_start_station_id = start_station_names[selected_start_station_name]

        selected_finish_station_name = st.selectbox("Select a finish station", list(finish_station_names.keys()))
        selected_finish_station_id = finish_station_names[selected_finish_station_name]

        # Проверка на пустые значения и отладочные сообщения
        st.write(f"Train ID: {selected_train_id}")
        st.write(f"Start Station ID: {selected_start_station_id}")
        st.write(f"Finish Station ID: {selected_finish_station_id}")

        # Создание маршрута
        if st.button("Create Route"):
            if selected_train_id and selected_start_station_id and selected_finish_station_id:
                try:
                    route_id = create_route(
                        selected_train_id, selected_start_station_id, selected_finish_station_id
                    )
                    st.success(f"Route created with ID {route_id}")
                except Exception as e:
                    st.error(f"Error occurred while creating route: {e}")
            else:
                st.error("Please select all fields to create a route.")
    
    # Показать маршруты по станции
    elif action == "View Routes by Station":
        st.subheader("View Routes by Station")
        
        stations = get_all_stations()  # Получаем все станции
        station_names = {station["name"]: station["id"] for station in stations}

        selected_station_name = st.selectbox("Select a station", list(station_names.keys()))
        selected_station_id = station_names[selected_station_name]

        if st.button("View Routes"):
            routes = get_routes_by_station(selected_station_id)
            if routes:
                st.write(f"Routes for Station '{selected_station_name}':")
                for route in routes:
                    st.write(f"**ID**: {route['id']}")
                    st.write(f"**Train Type**: {route['train_type']}")
                    st.write(f"**Start Station**: {route['start_station_name']}")
                    st.write(f"**Finish Station**: {route['finish_station_name']}")
                    st.write("---")
            else:
                st.info(f"No routes found for Station '{selected_station_name}'")

    # Показать все маршруты
    elif action == "View All Routes":
        st.subheader("View All Routes")

        routes = get_all_routes()
        if routes:
            st.write("All Routes:")
            for route in routes:
                st.write(f"**ID**: {route['id']}")
                st.write(f"**Train Type**: {route['train_type']}")
                st.write(f"**Start Station**: {route['start_station_name']}")
                st.write(f"**Finish Station**: {route['finish_station_name']}")
                st.write("---")
        else:
            st.info("No routes available")

    # Показать детали маршрута
    elif action == "View Route Details":
        st.subheader("View Route Details")

        route_id = st.number_input("Enter Route ID", min_value=1, step=1)

        if st.button("View Route"):
            route_details = get_route_by_id(route_id)
            if route_details:
                st.write(f"**Route ID**: {route_details['id']}")
                st.write(f"**Train ID**: {route_details['train_id']}")
                st.write(f"**Train Type**: {route_details['train_type']}")
                st.write(f"**Start Station**: {route_details['start_station_name']}")
                st.write(f"**Finish Station**: {route_details['finish_station_name']}")
            else:
                st.info(f"No route found for ID {route_id}")
