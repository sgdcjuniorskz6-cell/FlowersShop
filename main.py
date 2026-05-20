import json
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import WebAppInfo

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8303770835:AAExGk3ohqt73XsSnz1rzyHtB_gaowNgytk'
ADMIN_ID = 1482323384
WEB_APP_URL = "https://sgdcjuniorskz6-cell.github.io/FlowersShop/"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    welcome_text = (
        f"Приветствую вас, господин {message.from_user.first_name}! 🎩\n\n"
        "Добро пожаловать в обновленный премиальный бутик FLORISTIQUE.\n"
        "Мы полностью обновили интерфейс нашего приложения для вашего удобства. "
        "Теперь выбирать цветы стало еще приятнее и быстрее.\n\n"
        "Нажмите кнопку ниже, чтобы открыть наш новый каталог."
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Открыть каталог 💐", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    await message.answer(welcome_text, reply_markup=markup)

@dp.message_handler(content_types='web_app_data')
async def handle_order(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        report = (
            "🔔 ПОСТУПИЛ НОВЫЙ VIP-ЗАКАЗ\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚜️ Товар: {data['flower']}\n"
            f"🔢 Количество: {data['count']} шт.\n"
            f"📍 Адрес доставки: {data['address']}\n"
            f"💰 Бюджет клиента: {data['budget']} ₸\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Заказчик: @{message.from_user.username or 'Скрыт'}\n"
            f"🆔 ID пользователя: {message.from_user.id}"
        )
        
        # Отправляем админу
        await bot.send_message(ADMIN_ID, report)
        
        # Ответ клиенту
        await message.answer("Благодарю за выбор нашего салона, господин! Ваш заказ принят в обработку. Менеджер уже связывается с вами.")
        
    except Exception as e:
        logging.error(f"Ошибка при обработке заказа: {e}")
        await message.answer("Произошла ошибка при передаче заказа. Пожалуйста, попробуйте еще раз.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)