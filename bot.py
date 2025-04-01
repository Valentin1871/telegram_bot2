import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "7917679321:AAHntxbCrhmDjJTgW0NPpcsNBephC6fZQXg"
ADMIN_ID = 443615554
bot = telebot.TeleBot(TOKEN)

# Словник для тимчасового збереження даних
user_data = {}


# Вітання нового учасника в групі
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    user_id = message.new_chat_members[0].id
    bot.send_message(user_id, "👋 Вітаємо у групі! Для продовження вам потрібно зареєструватися.")

    # Запускаємо реєстрацію
    request_name(user_id)


# Запит імені
def request_name(user_id):
    msg = bot.send_message(user_id, "Введіть ваше ім'я:")
    bot.register_next_step_handler(msg, request_surname)


# Запит прізвища
def request_surname(message):
    user_data[message.chat.id] = {"name": message.text}
    msg = bot.send_message(message.chat.id, "Введіть ваше прізвище:")
    bot.register_next_step_handler(msg, request_phone)


# Запит номера телефону
def request_phone(message):
    user_data[message.chat.id]["surname"] = message.text

    # Кнопка для відправки контакту
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = KeyboardButton("📞 Надіслати контакт", request_contact=True)
    markup.add(contact_button)

    msg = bot.send_message(message.chat.id, "Надішліть ваш номер телефону:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_registration)


# Отримання та збереження контактних даних
@bot.message_handler(content_types=['contact'])
def save_registration(message):
    user_id = message.chat.id
    if user_id in user_data:
        user_data[user_id]["phone"] = message.contact.phone_number

        # Формуємо повідомлення для адміністратора
        registration_info = (
            f"📝 Нова реєстрація:\n"
            f"👤 Ім'я: {user_data[user_id]['name']}\n"
            f"👥 Прізвище: {user_data[user_id]['surname']}\n"
            f"📞 Телефон: {user_data[user_id]['phone']}\n"
        )

        # Надсилаємо адміністратору
        bot.send_message(ADMIN_ID, registration_info)

        # Відповідаємо користувачу
        bot.send_message(user_id, "✅ Реєстрація завершена! Дякуємо!")

        # Очищаємо тимчасові дані
        del user_data[user_id]


bot.polling(none_stop=True)
