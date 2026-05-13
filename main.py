import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import WebAppInfo

API_TOKEN = '8303770835:AAExGk3ohqt73XsSnz1rzyHtB_gaowNgytk'
ADMIN_ID = '1482323384' # Сюда придут заказы

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Приветственный текст
    welcome_text = (
        f"Приветствую вас, господин {message.from_user.first_name}!\n\n"
        "Добро пожаловать в наш элитный цветочный салон. 🌸\n"
        "У нас вы найдете не только роскошные букеты, но и экзотические растения, "
        "а также одиночные цветы для любого повода.\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог и оформить заказ."
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Замените ссылку на вашу от GitHub Pages
    web_app = WebAppInfo(url="https://sgdcjuniorskz6-cell.github.io/FlowersShop/")
    markup.add(types.KeyboardButton("Перейти в каталог 💐", web_app=web_app))
    
    await message.answer(welcome_text, reply_markup=markup)

@dp.message_handler(content_types='web_app_data')
async def get_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    order_text = (
        f"🔔 НОВЫЙ ЗАКАЗ!\n"
        f"--------------------------\n"
        f"Товар: {data['flower']}\n"
        f"Количество: {data['count']}\n"
        f"Адрес: {data['address']}\n"
        f"Бюджет: {data['budget']} ₸\n"
        f"--------------------------\n"
        f"Заказчик: @{message.from_user.username or 'ID: ' + str(message.from_user.id)}"
    )
    
    await bot.send_message(ADMIN_ID, order_text)
    await message.answer("Благодарим за заказ, господин! Администратор свяжется с вами в ближайшее время.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)