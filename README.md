# Train booking

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   
2. Создание бд:
   ```bash
   psql -h localhost -U postgres -c "CREATE DATABASE train_booking_kp;"

3. Примените миграции:   
    ```bash
    psql -U postgres -d train_booking_kp -f migrations/ddl.sql
    psql -U postgres -d train_booking_kp -f migrations/dml.sql

4. Запустите приложение:
   ```bash
   streamlit run main.py