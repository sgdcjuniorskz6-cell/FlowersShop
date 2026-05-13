import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import WebAppInfo

API_TOKEN = 'ВАШ_ТОКЕН'
ADMIN_ID = 'ВАШ_ID' # Сюда будут падать заказы

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # URL должен быть HTTPS. Для тестов используйте GitHub Pages или Ngrok.
    web_app = WebAppInfo(url="https://your-domain.com/index.html")
    markup.add(types.KeyboardButton("Открыть магазин", web_app=web_app))
    await message.answer(f"Приветствую, господин! Нажмите кнопку ниже для заказа.", reply_markup=markup)

@dp.message_handler(content_types='web_app_data')
async def get_data(message: types.Message):
    # Получаем данные из Mini App
    data = json.loads(message.web_app_data.data)
    
    order_text = (
        f"🔔 НОВЫЙ ЗАКАЗ!\n\n"
        f"Цветы: {data['flower']}\n"
        f"Адрес: {data['address']}\n"
        f"Количество: {data['count']}\n"
        f"Бюджет: {data['budget']} ₸\n"
        f"Заказчик: @{message.from_user.username}"
    )
    
    # Отправляем администратору
    await bot.send_message(ADMIN_ID, order_text)
    # Отправляем пользователю подтверждение и ссылку на оплату
    await message.answer("Ваш заказ принят! Администратор скоро свяжется с вами для оплаты.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)