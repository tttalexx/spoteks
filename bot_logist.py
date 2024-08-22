import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Настройка доступа к Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Подключение к таблицам
orders_sheet = client.open_by_key('1dPzPafixMYR8h0pgCSA5v7EGEEuqsZBGbC58sS75yIo').worksheet("ORDERS")
logistic_sheet_main = client.open_by_key('1dPzPafixMYR8h0pgCSA5v7EGEEuqsZBGbC58sS75yIo').worksheet("LOGISTIC")
logistics_sheet_m = client.open_by_key('1ijiewj-1aW6BX8yqtrVCSPl12n1IbuMfWyPIvfB478g').worksheet("Логистика")
logistics_sheet_o = client.open_by_key('1uS8iEg3E2x1pLPk77wO2eHsJNGoOGb6zBr7gS12B9Vo').worksheet("Логистика")
logistics_sheet_i = client.open_by_key('167_zVtBzZgXuedj0Y08HYIzVaVLg0fcUdqkL6FtmVIo').worksheet("Логистика")

# Инициализация счетчиков
read_requests = 0
write_requests = 0

# Функция для получения строки для `order_id`
def get_row_numbers(logistic_sheet_main):
    global read_requests
    data = logistic_sheet_main.col_values(1)  # Чтение первой колонки с order_id
    read_requests += 1
    row_map = {order_id: idx + 1 for idx, order_id in enumerate(data)}
    return row_map

# Функция для удаления дубликатов заявок по `order_id`
def remove_duplicates(logistics_sheet, sheet_name):
    global read_requests, write_requests
    records = logistics_sheet.get_all_records()
    read_requests += 1
    seen_order_ids = set()
    rows_to_delete = []
    for idx, record in enumerate(records):
        order_id = record['order_id']
        if order_id in seen_order_ids:
            rows_to_delete.append(idx + 2)
        else:
            seen_order_ids.add(order_id)
    
    if rows_to_delete:
        rows_to_delete.reverse()
        for row in rows_to_delete:
            logistics_sheet.delete_rows(row)
        write_requests += len(rows_to_delete)  # Один запрос на каждое удаление
        print(f"Удалено {len(rows_to_delete)} дублирующих заявок в {sheet_name}.")

# Функция для удаления заявки из таблиц логистов, если она была удалена в основной таблице
def remove_deleted_orders(main_order_ids, logistics_sheet, sheet_name):
    global read_requests, write_requests
    records = logistics_sheet.get_all_records()
    read_requests += 1
    rows_to_delete = []
    for idx, record in enumerate(records):
        if record['order_id'] not in main_order_ids:
            rows_to_delete.append(idx + 2)

    if rows_to_delete:
        rows_to_delete.reverse()
        for row in rows_to_delete:
            logistics_sheet.delete_rows(row)
        write_requests += len(rows_to_delete)  # Один запрос на каждое удаление
        print(f"Удалено {len(rows_to_delete)} заявок из {sheet_name}, которые были удалены в главной таблице.")

# Функция для сравнения значений в столбцах АВТО МАРИНА, АВТО ОЛЕГ, АВТО ИРИНА и записи минимального значения в АВТО мин
def update_auto_min_column():
    global read_requests, write_requests
    data = logistic_sheet_main.get_all_records()
    read_requests += 1