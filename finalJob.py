import telebot
from telebot import types


token = '7917746739:AAGb16veqs4-xGoqVW6IlyPLhqq8sZUzZL4'
ADMIN_USER_ID = 228718620
bot = telebot.TeleBot(token)


#Создаём словарь
exercises = {
    '🏃‍♂️‍➡️Кардио': 1000,
    '💪Силовая тренировка': 2000,
    '🧘Йога': 1500,
    '🤸Растяжка': 1200
}

user_data = {} #пустой словарь для хранения ифнормации от пользователя

#Функция для обработки команды "start"
def start_handler(message):
  welcome_message ='Добро пожаловац!'
  bot.send_message(message.chat.id, welcome_message)
  show_exercises_menu(message)

def show_exercises_menu(message):
  markup = types.InlineKeyboardMarkup()
  for exercise, price in exercises.items(): #как программа понимает что значит переменная 'price'
    button_text = exercise + '-' + str(price) + 'руб.'
    markup.add(types.InlineKeyboardButton(button_text, callback_data=exercise))
  bot.send_message(message.chat.id, 'Пожалуйста, выберите тренировку:',
                   reply_markup=markup) #как переносить строки

#Функция для обработки нажатия на кнопки, выбора тренировки
def exercise_selected(call): #call это объект из библиотеки telebot, который создаётся, когда пользователь нажимает на кнопку
  exercise = call.data
  price = exercises[exercise]
  user_data[call.message.chat.id] = {'exercise': exercise}
  bot.send_message(call.message.chat.id, 'Вы выбрали:' + '-' + exercise + '-' +
                   str(price) + '\nДля записи на тенировку, введите ваш номер телефона: ')
  bot.register_next_step_handler(call.message, get_phone_number) #установили привязку к следующему шагу обработчика


#пишем функцию для получения номера телефона
def get_phone_number(message):
  phone_number = message.text
  user_data[message.chat.id]['phone_number'] = phone_number
  bot.send_message(message.chat.id,
                   'Введите желаемую дату и время для зантятия: ')
  bot.register_next_step_handler(message, get_date_time)  #почему в этой функции убрали 'call'?


def get_date_time(message):
  date_time = message.text
  user_data[message.chat.id]['date_time'] = date_time
  exercise = user_data[message.chat.id]['exercise'] #Извелeчём ранее сохранённыe данные из словаря user_data
  phone_number = user_data[message.chat.id]['phone_number']
  bot.send_message(message.chat.id,
                   'Спасибо! Вы записались на ' + date_time + ' на ' + exercise +
                   '\nЯ свяжусь с Вами по номеру ' + phone_number + ' для уточнения деталей')
  bot.send_message(ADMIN_USER_ID, 'Новая запись: \nТренировка: ' + exercise + '\nДата и время: ' + date_time
                    + '\nНомер телефона: ' + phone_number)
  send_image(message)


def send_image(message):
  print('Функция работает')
  image_path = r'C:\Users\1\Desktop\Python Обучение\01.04. Финальная работа\Как подготовиться к тренировке.jpg' # Замените на путь к вашему изображению
  with open(image_path, 'rb') as image:
      bot.send_photo(message.chat.id, image, caption="Ознакомьтесь, пожалуйста, с памяткой о подготовке к тренировке.")



#Регистрация обработчика для команды /start
bot.register_message_handler(start_handler, commands=['start'])
#Регистрация обработчика для нажатия кнопок
bot.register_callback_query_handler(exercise_selected, func=lambda call: call.data in exercises.keys())
#Регистрация обработчика контактных данных
bot.register_message_handler(get_phone_number, content_types=['contact'])

#Запуск бота
bot.infinity_polling(none_stop=True)