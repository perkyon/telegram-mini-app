import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor

API_TOKEN = '7034849085:AAEktvROGNHpbKQV6BNfPZZPXuQbmhOxFD0'
PROVIDER_TOKEN = 'YOUR_PROVIDER_TOKEN'  # Полученный от вашего платежного провайдера

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Нажмите кнопку ниже для оплаты через мини-приложение.", reply_markup=main_menu())

def main_menu():
    keyboard = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton(text="Оплатить через Mini App", web_app=WebAppInfo(url="https://ваш_пользователь.github.io/telegram-mini-app/"))
    keyboard.add(web_app_button)
    return keyboard

@dp.message_handler(commands=['pay'])
async def process_pay_command(message: types.Message):
    prices = [LabeledPrice(label='Оплата услуги', amount=1000)]  # Цена в минимальных единицах валюты (например, 1000 = $10.00)
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Оплата услуги',
        description='Описание вашей услуги',
        payload='some-payload',
        provider_token=PROVIDER_TOKEN,
        currency='USD',
        prices=prices,
        start_parameter='test-payment',
        photo_url='https://example.com/photo.jpg',  # URL изображения
        photo_height=512,  # Высота изображения
        photo_width=512,  # Ширина изображения
        photo_size=512,  # Размер изображения
    )

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    if pre_checkout_query.invoice_payload != 'some-payload':
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Что-то пошло не так...")
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    await message.reply("Оплата успешно завершена!")

@dp.message_handler(lambda message: message.web_app_data is not None)
async def handle_web_app_data(message: types.Message):
    web_app_data = message.web_app_data.data
    await message.answer(f"Получены данные из веб-приложения: {web_app_data}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
