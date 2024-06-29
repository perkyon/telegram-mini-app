import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

API_TOKEN = '7034849085:AAEktvROGNHpbKQV6BNfPZZPXuQbmhOxFD0'
PROVIDER_TOKEN = 'YOUR_PROVIDER_TOKEN'  # Полученный от вашего платежного провайдера

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Привет! Нажмите кнопку ниже для оплаты через мини-приложение.", reply_markup=main_menu())

# Функция для создания главного меню
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить через Mini App", web_app={"url": "https://perkyon.github.io/telegram-mini-app/"})]
    ])
    return keyboard

# Обработчик команды /pay
@dp.message(Command('pay'))
async def process_pay_command(message: Message):
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

# Обработчик предпродажной проверки
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    if pre_checkout_query.invoice_payload != 'some-payload':
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Что-то пошло не так...")
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработчик успешной оплаты
@dp.message(lambda message: message.successful_payment is not None)
async def process_successful_payment(message: Message):
    await message.answer("Оплата успешно завершена!")

# Обработчик данных из Web App
@dp.message(lambda message: message.web_app_data is not None)
async def handle_web_app_data(message: Message):
    web_app_data = message.web_app_data.data
    await message.answer(f"Получены данные из веб-приложения: {web_app_data}")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
