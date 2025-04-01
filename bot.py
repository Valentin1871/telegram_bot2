import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7917679321:AAHntxbCrhmDjJTgW0NPpcsNBephC6fZQXg"
ADMIN_ID = "443615554"
GROUP_1_LINK = "https://t.me/+DDh_eTYqz9FhNzNi"  # Посилання на першу групу
GROUP_2_LINK = "https://t.me/zakutoksp"  # Посилання на другу групу

bot = telebot.TeleBot(TOKEN)
user_data = {}

# 🔹 Обробка команди /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "👋 Вітаємо! Для продовження потрібно зареєструватися.")
    request_name(message.chat.id)



# 🔹 Запит імені
def request_name(user_id):
    msg = bot.send_message(user_id, "Введіть ваше ім'я:")
    bot.register_next_step_handler(msg, request_surname)


# 🔹 Запит прізвища
def request_surname(message):
    user_id = message.chat.id
    user_data[user_id] = {"name": message.text}

    msg = bot.send_message(user_id, "Введіть ваше прізвище:")
    bot.register_next_step_handler(msg, request_phone)


# 🔹 Запит номера телефону
def request_phone(message):
    user_id = message.chat.id
    user_data[user_id]["surname"] = message.text

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = KeyboardButton("📞 Надіслати контакт", request_contact=True)
    markup.add(contact_button)

    msg = bot.send_message(user_id, "Надішліть ваш номер телефону:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_registration)


# 🔹 Отримання контакту та збереження реєстрації
@bot.message_handler(content_types=['contact'])
def save_registration(message):
    user_id = message.chat.id

    if message.contact is None:
        bot.send_message(user_id, "⚠ Будь ласка, скористайтеся кнопкою для надсилання контакту.")
        request_phone(message)
        return

    user_data[user_id]["phone"] = message.contact.phone_number

    # 🔹 Формуємо повідомлення для адміністратора
    registration_info = (
        f"📝 Нова реєстрація:\n"
        f"👤 Ім'я: {user_data[user_id]['name']}\n"
        f"👥 Прізвище: {user_data[user_id]['surname']}\n"
        f"📞 Телефон: {user_data[user_id]['phone']}\n"
    )

    bot.send_message(ADMIN_ID, registration_info)  # 🔹 Надсилаємо адміну
    bot.send_message(user_id, "✅ Реєстрація завершена! Дякуємо!")

    # 🔹 Надсилаємо посилання на групи
    bot.send_message(user_id, f"🌍 Долучайтесь до наших груп:\n🔗 {GROUP_1_LINK}\n🔗 {GROUP_2_LINK}")

    del user_data[user_id]  # Очищаємо тимчасові дані


bot.polling(none_stop=True)
