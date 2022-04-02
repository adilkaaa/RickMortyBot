import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from random import randint
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre
# from rick import get_character_info as info


def get_character_data_by_name(name):
    response = requests.get(f"https://rickandmortyapi.com/api/character"
                            f"/?name={name.lower()}")

    if response.status_code == 404:
        raise Exception('Not found!(')

    return response.json()
def get_character_info(name):
    # name = input("enter character name please: ")
    data = get_character_data_by_name(name)
    character = data['results'][0]

    return {
    'name': character['name'],
    'status': character['status'],
    'species': character['species'],
    'type': character['type'],
    'gender': character['gender'],
    'img': character['image'],
    'location': character['location']['name'],
    'episode': character['episode'][0]
    }


API_TOKEN = '5286162477:AAFw1JQme44zx1ISctGH3xmbS-Okq9z-Ee8'


bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def send_hello(message: types.Message):
    await message.reply("""Hi, I am RickMortyBot. \n
    I could get information for any charters of 'Rick and Morty'.\n
    You could type /help for information.""")

@dp.message_handler(commands='help')
async def show_info(message: types.Message):
    await message.answer("""
    all commands:\n
    /help - show all commands \n
    /getcharacter - gives info about character\n
    /start - starts the bot
    """)

@dp.message_handler(commands = 'getcharacter')
async def show_list_characters(message: types.Message):
    # await message.answer('Choose character:')
    keyboard_inline = types.InlineKeyboardMarkup()
    c1 = types.InlineKeyboardButton(text='Rick Sanchez',callback_data='rick sanchez')
    c2 = types.InlineKeyboardButton(text='Morty Smith',callback_data='morty smith')
    c3 = types.InlineKeyboardButton(text='Summer Smith',callback_data='summer smith')
    c4 = types.InlineKeyboardButton(text='Jerry Smith',callback_data='jerry smith')
    c5 = types.InlineKeyboardButton(text='Squanchy',callback_data='squanchy')
    c6 = types.InlineKeyboardButton(text='Beth Smith',callback_data='beth smith')
    c7 = types.InlineKeyboardButton(text='Krombopulos Michael',callback_data='krombopulos michael')
    c8 = types.InlineKeyboardButton(text='Reverse Giraffe',callback_data='reverse giraffe')
    c9 = types.InlineKeyboardButton(text='Birdperson',callback_data='birdperson')
    keyboard_inline.add(c1,c2,c3,c4,c5,c6,c7,c8,c9)
    await message.answer('Choose one of them\n',reply_markup=keyboard_inline)

@dp.callback_query_handler(text = ['rick sanchez','morty smith','summer smith','jerry smith','squanchy','beth smith','krombopulos michael','reverse giraffe','birdperson'])
async def answer(call: types.CallbackQuery):
    char = get_character_info(call.data)
    name = char['name']
    img = char['img']
    gender = char['gender']
    location = char['location']
    status = char['status']
    species = char['species']
    episode = char['episode']
    t = char['type']
    await call.message.answer_photo(img)

    await call.message.answer(f"""    <b>Name: {name}\n
Gender: {gender}\n
Status: {status}\n
Type: {t}\n
Species: {species}\n
Location: {location}\n
Episode: {str(episode)}\n
Continue chosing /getcharacter</b>""",parse_mode=ParseMode.HTML)
    

    







if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)

