import telebot
from telebot import types
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from random import randint
from english_words import english_words_lower_alpha_set
from random import choice


bot = telebot.TeleBot('my token',parse_mode=None)
config_dict = get_default_config()
config_dict['language']='eng'
owm = OWM('95552b3ea478bf1a0b5ceb47b2681758')
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    sti = open('C://Users//yegor//Desktop//Bot//приветик.webp','rb')
    bot.send_sticker(message.chat.id,sti)
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Weather')
    button_2 = types.KeyboardButton('How is it going?')
    button_3 = types.KeyboardButton('Play a game')
    button_4 = types.KeyboardButton('The word of the day')
    key.add(button_1,button_2,button_3,button_4)
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id,f'Hello, {user_first_name}',parse_mode='html',reply_markup=key)
    bot.send_message(message.chat.id,'My name is Kuzmich. I am the Telegram Bot and I can do various things. Now I am going to show you what I can do (you will see buttons on your keyboard).')
    bot.send_message(message.chat.id,'Weather - to find out the weather of a city you enter. Play a game - to guess a random number from 1 to 100. How is it going? - to ask how your life is going. The word of the day - to print a random English word in order to increase your vocabulary')
    bot.send_message(message.chat.id,'If you press a button and nothing works, then do not worry. The bot is in progress and there can be  some mistakes. Just  press the button you need once again)')
@bot.message_handler(content_types = ['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'How is it going?':
            markup = types.InlineKeyboardMarkup()
            good = types.InlineKeyboardButton('It is great!',callback_data='good')
            bad = types.InlineKeyboardButton('Awful(',callback_data='bad')
            markup.add(good,bad)
            bot.send_message(message.chat.id,'Everyting is nice! What about you?',reply_markup=markup)
        elif message.text == 'Weather':  
            def answer(city):
                try:
                    city = city.text
                    mgr = owm.weather_manager()
                    observation = mgr.weather_at_place(city)
                    w = observation.weather
                    temp = w.temperature('celsius')['temp']
                    bot.send_message(message.chat.id,f'{w.detailed_status} in {city}')
                    bot.send_message(message.chat.id,f'The temperature is {temp}')
                    bot.send_message(message.chat.id,'Use /start to call the menu')
                except NotFoundError:
                        bot.send_message(message.chat.id,'The bot could not find your city:( Use /start to call the menu and to enter a city once again')
            city =  bot.send_message(message.chat.id,'Enter your city:')
            bot.register_next_step_handler(city,answer)
        elif message.text == 'The word of the day':
            words = sorted([i for i in english_words_lower_alpha_set])
            word_of_the_day = choice(words)
            bot.send_message(message.chat.id,f'The word of the day is {word_of_the_day}')
    
        elif message.text=='Play a game':
            def game(number):
                number = int(number.text)
                if number==random_number:
                    bot.send_message(message.chat.id,'Congratulations')
                    bot.send_message(message.chat.id,'Use /start to call the menu')
                else:
                    if number<random_number:
                        bot.send_message(message.chat.id,'The number is bigger than yours')
                    else:
                        bot.send_message(message.chat.id,'The number is smaller than yours')
                    number = bot.send_message(message.chat.id,'Enter a number')
                    bot.register_next_step_handler(number,game)
            number = bot.send_message(message.chat.id,'Enter a number')
            random_number = randint(1,100+1)
            bot.register_next_step_handler(number,game)
        else:
            bot.send_message(message.chat.id,'I do not understand you:(')

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data=='good':
        bot.send_message(call.message.chat.id,'Awesome:)')
        bot.send_message(call.message.chat.id,'Use /start to call the menu')
    
    elif call.data == 'bad':
        bot.send_message(call.message.chat.id,'It sometimes happens:(')
        bot.send_message(call.message.chat.id,'Use /start to call the menu')
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text='How is it going?',reply_markup=None)




bot.infinity_polling()