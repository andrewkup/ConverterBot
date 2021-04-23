import telebot
from config import exchanger, TOKEN
from extensions import Converter, ConverterException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты>  \
<в какую валюту перенести> \
<количество переводимой валюты>\nУвидеть список все доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text += '\n'.join(f'{i+1}) {key}' for i, key in enumerate(exchanger.keys()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Converter.get_price(values)
    except ConverterException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} -- {result} {exchanger[values[1]]}'
        bot.reply_to(message, text)


bot.polling()