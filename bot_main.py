import nest_asyncio
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot_auth import handle_orders, contact_handler, handle_name_registration, show_main_menu
from bot_actual_price import show_prices
from bot_orders import show_user_orders, create_order_conversation_handler
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Применение nest_asyncio для совместимости с уже запущенными циклами событий
nest_asyncio.apply()

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Настройки Telegram Bot API
bot_token = '6679900044:AAGDIGrEGjq_jTK3_5tzXm_qGLLNuCY4Tgc'

# Настройки Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client_gsheets = gspread.authorize(creds)
sheet_prices = client_gsheets.open_by_key("1dPzPafixMYR8h0pgCSA5v7EGEEuqsZBGbC58sS75yIo").worksheet("actual_price")

# Функция-обертка для передачи аргумента sheet_prices
async def show_prices_wrapper(update, context):
    await show_prices(update, context, sheet_prices)

# Основная функция запуска бота
async def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", show_main_menu))  # Обработчик команды /start
    application.add_handler(MessageHandler(filters.Regex("Актуальные цены"), show_prices_wrapper))
    application.add_handler(MessageHandler(filters.Regex("Заявки"), handle_orders))
    application.add_handler(MessageHandler(filters.Regex("Мои заявки"), show_user_orders))
    application.add_handler(create_order_conversation_handler())
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_registration))

    logger.info("Бот запущен и ожидает команд...")
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")