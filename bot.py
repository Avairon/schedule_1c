import telebot
from telebot import types
import threading
import time
import data.core as core  # Ваш модуль с функциями

# Инициализация бота
bot = telebot.TeleBot('7398324831:AAGg9ULjsKF6eEiuNasBWDjpwZF0PgR9doY')  # Замените '!!!' на токен вашего бота

# Функция для периодического обновления состояния в консоли
def console_update():
    while True:
        core.watch_pup()  # Вывод текущего состояния в консоль
        time.sleep(1)  # Обновление каждую секунду

# Запуск потока для обновления консоли
console_thread = threading.Thread(target=console_update, daemon=True)
console_thread.start()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Insert")
    btn2 = types.KeyboardButton("Remove")
    btn3 = types.KeyboardButton("Catch")
    btn4 = types.KeyboardButton("Search")
    btn5 = types.KeyboardButton("Watch")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, "Welcome to the Pupiryshki Bot!", reply_markup=markup)

# Обработка текстовых команд
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "Insert":
        bot.send_message(message.chat.id, "Please enter the name, count, and type of pupiryshki.")
        bot.register_next_step_handler(message, insert_pup)

    elif message.text == "Remove":
        bot.send_message(message.chat.id, "Please enter the name of the pupiryshki to remove.")
        bot.register_next_step_handler(message, remove_pup)

    elif message.text == "Catch":
        bot.send_message(message.chat.id, "Please enter the name of the pupiryshki to catch.")
        bot.register_next_step_handler(message, catch_pup)

    elif message.text == "Search":
        bot.send_message(message.chat.id, "Please enter the name of the pupiryshki to search.")
        bot.register_next_step_handler(message, search_pup)

    elif message.text == "Watch":
        try:
            # Получаем текущее состояние предметов в виде текста
            pups_text = core.get_pups_as_text()

            # Отправляем сообщение пользователю
            bot.send_message(message.chat.id, pups_text)
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}")

# Функция для добавления записи
def insert_pup(message):
    try:
        name, count, type_ = message.text.split()
        core.json_write(name, int(count), type_)
        bot.send_message(message.chat.id, f"Added {name} {count} {type_}")
    except Exception as e:
        bot.send_message(message.chat.id, "Error! Please enter data in the format: name count type")

# Функция для удаления записи
def remove_pup(message):
    result = core.remove_pup(message.text)
    if result["pup_name"]:
        bot.send_message(message.chat.id, f"Removed {result['pup_name']} {result['pup_count']}")
    else:
        bot.send_message(message.chat.id, "Pupiryshki not found!")

# Функция для "захвата" записи
# Функция для "захвата" записи
def catch_pup(message):
    try:
        # Разбиваем сообщение на имя и количество
        name, count_to_catch = message.text.split()
        count_to_catch = int(count_to_catch)  # Преобразуем количество в число

        # Вызываем функцию из core.py
        success = core.catch_pup(name, count_to_catch)

        if success:
            bot.send_message(message.chat.id, f"Successfully caught {count_to_catch} of {name}.")
        else:
            bot.send_message(message.chat.id, "Failed to catch items. Check the console for details.")
    except ValueError:
        bot.send_message(message.chat.id, "Error! Please enter data in the format: name count")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Функция для поиска записи
def search_pup(message):
    core.search_pup(message.text)
    bot.send_message(message.chat.id, "Search completed. Check the console for details.")

# Запуск бота
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)