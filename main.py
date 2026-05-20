import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8303770835:AAExGk3ohqt73XsSnz1rzyHtB_gaowNgytk'
ADMIN_ID =  1482323384
WEB_APP_URL = "https://sgdcjuniorskz6-cell.github.io/FlowersShop/?v=3"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    welcome_text = (
        f"Приветствую вас, господин {message.from_user.first_name}! 🎩\n\n"
        "Добро пожаловать в обновленный премиальный бутик FLORISTIQUE.\n"
        "Мы полностью обновили интерфейс нашего приложения для вашего удобства. "
        "Теперь выбирать цветы стало еще приятнее и быстрее.\n\n"
        "Нажмите кнопку ниже, чтобы открыть наш новый каталог."
    )
    
    # ИСПРАВЛЕНО: Правильное создание клавиатуры без опечаток
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Открыть каталог 💐", web_app=types.WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True
    )
    
    await message.answer(welcome_text, reply_markup=markup)

# Хендлер получения данных из Mini App
@dp.message(F.web_app_data)
async def handle_order(message: types.Message):
    try:
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        
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
        
        # Бот САМ пишет вам как администратору
        await bot.send_message(chat_id=ADMIN_ID, text=report)
        
        # Бот САМ пишет клиенту в чат
        await message.answer("Благодарю за выбор нашего салона, господин! Ваш заказ принят в обработку. Менеджер уже связывается с вами.")
        
    except Exception as e:
        logging.error(f"Ошибка при обработке заказа: {e}")
        await message.answer("Произошла ошибка при передаче заказа. Пожалуйста, попробуйте еще раз.")

async def main():
    print("Сбрасываем конфликтующие вебхуки...")
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен в VS Code!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())