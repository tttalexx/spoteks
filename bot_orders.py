import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
import logging
from datetime import datetime

# Настройки логирования
logger = logging.getLogger(__name__)

# Фиксированный список областей
REGIONS = [
    "Винницкая", "Волынская", "Днепропетровская", "Донецкая", "Житомирская", "Закарпатская", 
    "Запорожская", "Ивано-Франковская", "Киев", "Киевская", "Кировоградская", "Луганская", 
    "Львовская", "Николаевская", "Одесская", "Полтавская", "Ровенская", "Сумская", 
    "Тернопольская", "Харьковская", "Херсонская", "Хмельницкая", "Черкасская", 
    "Черниговская", "Черновицкая"
]

# Открытие листа с заявками и другими данными
def open_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client_gsheets = gspread.authorize(creds)
    return client_gsheets.open_by_key("1dPzPafixMYR8h0pgCSA5v7EGEEuqsZBGbC58sS75yIo").worksheet(sheet_name)

sheet_orders = open_sheet("ORDERS")
sheet_users = open_sheet("db_users")
sheet_culture = open_sheet("db_culture")

# Константы состояний
(SELECT_CULTURE, INPUT_VOLUME, SELECT_DELIVERY, INPUT_PRICE, SELECT_REGION, INPUT_LOAD_PLACE, 
 SELECT_UNLOAD_PLACE, INPUT_COMMENT, CONFIRM) = range(9)

# Функция для показа заявок пользователя
async def show_user_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_sid = get_user_sid(user.id)

    if not user_sid:
        await update.message.reply_text("Вы не зарегистрированы.")
        return

    orders_data = sheet_orders.get_all_values()
    user_orders = [row for row in orders_data if row[0] == user_sid]  # user_sid в столбце A

    if not user_orders:
        await update.message.reply_text("У вас нет заявок.")
        return

    message_text = "Ваши заявки:\n\n"
    for order in user_orders:
        order_number = order[3]  # Номер заявки - столбец D
        date = order[1]  # Дата - столбец B
        culture = order[4]  # Культура - столбец E
        volume = order[6]  # Объем - столбец G
        delivery = order[7]  # Условия поставки - столбец H
        price = order[8]  # Цена - столбец I
        region = order[13]  # Область загрузки - столбец N
        unload_place = order[15]  # Место выгрузки - столбец P
        status = order[12]  # Статус заявки - столбец M
        additional_info = order[17]  # Дополнительная информация - столбец R

        # Форматирование вывода заявки
        order_message = (
            f"🔹 #{order_number} {date}\n"
            f"{culture} {volume}т\n"
            f"{delivery} {price} грн/т\n"
            f"{region}\n"
            f"{unload_place}\n"
            f"Статус: {status}\n"
        )