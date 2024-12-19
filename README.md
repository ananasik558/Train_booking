# Train booking

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   

2. Примените миграции:   
    ```bash
    psql -U postgres -d train_booking_kp -f migrations/ddl.sql
    psql -U postgres -d train_booking_kp -f migrations/dml.sql

3. Запустите приложение:
   ```bash
   streamlit run main.py