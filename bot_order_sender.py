sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Храним предыдущее состояние столбца
last_parsed_values = []
total_sent_messages = 0
new_messages_count = 0
update_messages_count = 0

def fetch_data():
    """Функция для получения данных из Google Sheets."""
    col_values = sheet.col_values(sheet.find("parsTOgroup").col)[1:]  # исключаем заголовок
    return col_values

def check_for_updates():
    global last_parsed_values, total_sent_messages, new_messages_count, update_messages_count

    # Получаем данные из Google Sheets
    col_values = fetch_data()

    # Если это первый запуск, сохраняем текущее состояние
    if not last_parsed_values:
        last_parsed_values = col_values
        return

    # Проверка изменений
    sent_messages = []
    for i, value in enumerate(col_values):
        if i >= len(last_parsed_values):
            # Новая информация
            message = f"new! {value}"
            bot.send_message(CHAT_ID, message, parse_mode='Markdown')
            total_sent_messages += 1
            new_messages_count += 1
            sent_messages.append(message)
        elif value != last_parsed_values[i]:
            # Обновление информации
            updated_value = f"update! __{value}__"  # Подчеркиваем обновленную информацию
            message = updated_value
            bot.send_message(CHAT_ID, message, parse_mode='Markdown')
            total_sent_messages += 1
            update_messages_count += 1
            sent_messages.append(message)

    # Обновляем сохраненные значения
    if sent_messages:
        last_parsed_values = col_values

    # Логируем отправленные сообщения
    if sent_messages:
        print(f"Отправлено сообщений: {len(sent_messages)}. Новых: {new_messages_count}. Обновлений: {update_messages_count}.")

def log_status():
    """Функция для логирования текущего статуса бота."""
    print(f"bot_sender OK. Всего сообщений отправлено: {total_sent_messages}. Новых: {new_messages_count}. Обновлений: {update_messages_count}.")

# Запуск проверки каждые 30 секунд
schedule.every(30).seconds.do(check_for_updates)

# Логирование статуса каждые 10 минут
schedule.every(10).minutes.do(log_status)

# Сообщение о запуске бота
print("bot_sender start OK")

# Основной цикл работы бота
while True:
    schedule.run_pending()
    time.sleep(1)