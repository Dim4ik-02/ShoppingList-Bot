from api_token import API_TOKEN
import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot(API_TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, 'shoppingList.json')


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='UTF-8') as file:
            return json.load(file)
    return {}


def save_data(lst):
    with open(FILE_NAME, 'w', encoding='UTF-8') as file:
        json.dump(lst, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('Add')
    btn_show = types.KeyboardButton('Show')
    btn_clear = types.KeyboardButton('Clear')
    markup.row(btn_add, btn_show)
    markup.row(btn_clear)
    bot.send_message(message.chat.id, 
                    f'Hello! I am a bot that will help you with your shopping list. The list of all commands will be below:\n\n'
                    f'/start - Start a bot\n'
                    f'/add_item - Add an item to the list\n'
                    f'/show_list - Shows a list with your products\n'
                    f'/mark_as_bought - Marks an item in the list as bought\n'
                    f'/delete_item - Removes an item from list\n'
                    f'/clear_list - Clears the list completely\n'
                    f'/export_json - Sends the entire list as a json-file',
                    reply_markup=markup)


@bot.message_handler(commands=['add_item'])
def add(message):
    bot.send_message(message.chat.id, 'Enter product which you want to add (write "stop" if you finished)')
    bot.register_next_step_handler(message, add_item)


def add_item(message):
    user_id = str(message.from_user.id)
    if message.text.strip().lower() == 'stop':
        bot.send_message(message.chat.id, 'Adding is done')
    else:
        data = load_data()
        if user_id not in data:
            data[user_id] = []
        data[user_id].append({
            'number': len(data[user_id]) + 1,
            'item': message.text.strip().lower(),
            'done': False
        })
        save_data(data)
        bot.send_message(message.chat.id, 'Item added successfully. Anything else?')
        bot.register_next_step_handler(message, add_item)


@bot.message_handler(commands=['show_list'])
def show(message):
    show_list(message)


def show_list(message):
    user_id = str(message.from_user.id)
    data = load_data()
    output = ''
    if user_id in data and data[user_id]:
        for i in data[user_id]:
            output += f"{i['number']}. {i['item']} {'✅' if i['done'] else '❌'}\n"
        bot.send_message(message.chat.id, output)
    else:
        bot.send_message(message.chat.id, 'No data found')


@bot.message_handler(commands=['mark_as_bought'])
def mark_as_bought(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and data[user_id]:
        bot.send_message(message.chat.id, 'Enter product which you already bought')
        bot.register_next_step_handler(message, mark)
    else:
        bot.send_message(message.chat.id, 'List is empty')


def mark(message):
    user_id = str(message.from_user.id)
    data = load_data()
    for products in data[user_id]:
        if products['item'] == message.text.strip().lower():
            if products['done'] == False:
                products['done'] = True
                save_data(data)
                bot.send_message(message.chat.id, 'Product was marked successfully')
                break
    else:
        bot.send_message(message.chat.id, 'No such product in list or product already marked as bought') 


@bot.message_handler(commands=['delete_item'])
def delete_item(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and data[user_id]:
        bot.send_message(message.chat.id, 'Enter which product you want to delete')
        bot.register_next_step_handler(message, delete)
    else:
        bot.send_message(message.chat.id, 'List is empty or there is no such product in it')


def delete(message):
    user_id = str(message.from_user.id)
    data = load_data()
    for i, product in enumerate(data[user_id]):
        if product['item'] == message.text.strip().lower():
            del data[user_id][i]
            save_data(data)
            data = load_data()
            for i, product in enumerate(data[user_id]):
                product['number'] = i + 1
            save_data(data)
            bot.send_message(message.chat.id, 'Product was deleted successfully')
            break


@bot.message_handler(commands=['clear_list'])
def clear(message):
    clear_list(message)


def clear_list(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and data[user_id]:
        del data[user_id]
        save_data(data)
        bot.send_message(message.chat.id, 'List was cleared successfully!')
    else:
        bot.send_message(message.chat.id, 'List was already cleared')


@bot.message_handler(commands=['export_json'])
def export_json(message):
    try:
        with open(FILE_NAME, 'rb') as file:
            bot.send_document(message.chat.id, file, caption='Here is your file')
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'File not found')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {e}')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
        f'Here is a list of all available commands:\n\n'
        f'/start - Start a bot\n'
        f'/add_item - Add an item to the list\n'
        f'/show_list - Shows a list with your products\n'
        f'/mark_as_bought - Marks an item in the list as bought\n'
        f'/delete_item - Removes an item from list\n'
        f'/clear_list - Clears the list completely\n'
        f'/export_json - Sends the entire list as a json-file')


@bot.message_handler(content_types=['text'])
def random_input(message):
    if message.text.strip().lower() == 'add':
        bot.send_message(message.chat.id, 'Enter product which you want to add (write "stop" if you finished)')
        bot.register_next_step_handler(message, add_item)
    elif message.text.strip().lower() == 'show':
        show_list(message)
    elif message.text.strip().lower() == 'clear':
        clear_list(message)
    else:
        bot.send_message(message.chat.id, 'Oops... You wrote something wrong. Write /help to see all available commands')


bot.infinity_polling()