import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from database import Database
from keyboards import ReplyKeyboardMarkup, KeyboardButton
from character_creation import create_character, select_class, distribute_points, select_point, go_back_to_characteristics, finish_character_creation, select_backstory_type, write_backstory
from keyboards import get_main_menu_keyboard

API_TOKEN = '6749445836:AAF3BYbkaVuBvJP85Bau6Q5vZsQG5FlTAxg'

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize database
db = Database('characters.db')

# Define class options
classes = ['Warrior', 'Mage', 'Rogue', 'Cleric', 'Fighter', 'Thief', 'Paladin', 'Ranger']

# Define characteristic options
characteristics = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']

# Define point options
point_options = [15, 14, 13, 12, 10, 8]

# Define backstory types
backstory_types = ['Artist', 'Homeless child', 'Noble', 'Guild Artisan', 'Sailor', 'Sage', 'People\'s hero', 'Hermit', 'Pirate', 'Criminal', 'Minion', 'Soldier', 'Alien', 'Charlatan']

# Message handler for the start command
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the Character Creator! Please select an option:", reply_markup=get_main_menu_keyboard())

# Message handler for the main menu
@dp.message_handler(lambda message: message.text in ["Create New Character", "Edit Existing Character", "View Existing Characters"])
async def process_main_menu(message: types.Message):
    if message.text == "Create New Character":
        await message.reply("Let's start creating your character! Please send me your character's name.")
        message.bot['state'] = 'creating_character'
    elif message.text == "Edit Existing Character":
        character_names = db.get_all_character_names()
        if character_names:
            keyboard = get_character_keyboard(character_names)
            await message.reply("Please select a character to edit:", reply_markup=keyboard)
            message.bot['state'] = 'selecting_character_to_edit'
        else:
            await message.reply("There are no characters to edit.")
    elif message.text == "View Existing Characters":
        character_names = db.get_all_character_names()
        if character_names:
            keyboard = get_character_keyboard(character_names)
            await message.reply("Please select a character to view:", reply_markup=keyboard)
        else:
            await message.reply("There are no characters to view.")

# Function to create the character selection keyboard
def get_character_keyboard(character_names):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for name in character_names:
        keyboard.add(KeyboardButton(name))
    return keyboard

# Message handler for character name
@dp.message_handler(lambda message: message.bot.get('state') == 'creating_character')
async def process_name(message: types.Message):
    response, keyboard = create_character(message, classes, characteristics, point_options, backstory_types)
    await message.reply(response, reply_markup=keyboard)

# Message handler for selecting a character to view
@dp.message_handler(lambda message: message.text in db.get_all_character_names())
async def view_character(message: types.Message):
    character_name = message.text
    character_details = db.get_character_details(character_name)
    if character_details:
        character_info = f"Character Details for {character_name}:\n\n"
        character_info += f"Class: {character_details['class']}\n"
        character_info += f"Strength: {character_details['strength']}\n"
        character_info += f"Dexterity: {character_details['dexterity']}\n"
        character_info += f"Constitution: {character_details['constitution']}\n"
        character_info += f"Intelligence: {character_details['intelligence']}\n"
        character_info += f"Wisdom: {character_details['wisdom']}\n"
        character_info += f"Charisma: {character_details['charisma']}\n"
        character_info += f"\nBackstory ({character_details['backstory_type']}):\n{character_details['backstory']}"
        await message.reply(character_info)
    else:
        await message.reply("Character not found in the database.")

# Message handler for character class selection
@dp.message_handler(lambda message: message.bot.get('state') == 'asking_class' and message.text in classes)
async def process_class(message: types.Message):
    response, keyboard = select_class(message, message.text, characteristics, point_options)
    await message.reply(response, reply_markup=keyboard)

# Message handler for characteristic selection
@dp.message_handler(lambda message: message.bot.get('state') == 'distributing_points' and message.text in characteristics)
async def process_characteristic(message: types.Message):
    response, keyboard = distribute_points(message, message.text, point_options)
    await message.reply(response, reply_markup=keyboard)

# Message handler for point selection
@dp.message_handler(lambda message: message.bot.get('state') == 'selecting_point' and message.text.isdigit())
async def process_point(message: types.Message):
    response, keyboard = select_point(message, int(message.text), message.bot['selected_char'], point_options)
    await message.reply(response, reply_markup=keyboard)

# Message handler for going back to the characteristic selection menu
@dp.message_handler(lambda message: message.bot.get('state') == 'selecting_point' and message.text == 'Back')
async def go_back_to_characteristics(message: types.Message):
    response, keyboard = go_back_to_characteristics(message)
    await message.reply(response, reply_markup=keyboard)

# Message handler for finishing the character creation
@dp.message_handler(lambda message: message.bot.get('state') == 'distributing_points' and message.text == 'Done')
async def finish_character_creation(message: types.Message):
    response, keyboard = finish_character_creation(message, characteristics)
    await message.reply(response, reply_markup=keyboard)

# Message handler for backstory type selection
@dp.message_handler(lambda message: message.bot.get('state') == 'selecting_backstory_type' and message.text in backstory_types)
async def process_backstory_type(message: types.Message):
    character = message.bot['character']
    character['backstory_type'] = message.text
    await message.reply("Great! Now, please write your character's backstory:")
    message.bot['state'] = 'writing_backstory'

# Message handler for backstory type selection
@dp.message_handler(lambda message: message.bot.get('state') == 'selecting_backstory_type')
async def process_backstory_type(message: types.Message):
    if message.text in backstory_types:
        # Set the selected backstory type in the bot's data
        message.bot['selected_backstory_type'] = message.text
        # Set the state to 'writing_backstory'
        message.bot['state'] = 'writing_backstory'
        await message.reply(f"You have selected the backstory type: {message.text}\nPlease write your backstory:")
    else:
        await message.reply("Invalid backstory type. Please select a valid backstory type.")

# Message handler for backstory writing
@dp.message_handler(lambda message: message.bot.get('state') == 'writing_backstory')
async def process_backstory(message: types.Message):
    # Get the selected backstory type from the bot's data
    selected_backstory_type = message.bot.get('selected_backstory_type')
    if selected_backstory_type:
        # Call the write_backstory function to process the backstory
        character_info = write_backstory(message, message.text)
        # Reset the state and selected backstory type
        message.bot['state'] = None
        message.bot['selected_backstory_type'] = None
        # Send the character details to the user
        await message.reply(character_info)
    else:
        await message.reply("It seems there was an error. Please start the character creation process again.")

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
    logging.info("Bot stopped.")