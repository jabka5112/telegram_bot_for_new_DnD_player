from database import save_character_to_db, backstory_types
from keyboards import get_class_keyboard, get_characteristic_keyboard, get_point_keyboard, get_backstory_type_keyboard

def create_character(message, classes, characteristics, point_options, backstory_types):
    message.bot['character'] = {'name': message.text}
    message.bot['state'] = 'asking_class'
    return f"Great! Now, please choose your character's class:", get_class_keyboard(classes)

def select_class(message, selected_class, characteristics, point_options):
    character = message.bot['character']
    character['class'] = selected_class
    character['points'] = {char: list(point_options) for char in characteristics}
    message.bot['state'] = 'distributing_points'
    return f"Now, select a characteristic to distribute points:", get_characteristic_keyboard(character['points'])

def distribute_points(message, selected_char, available_points):
    message.bot['selected_char'] = selected_char
    message.bot['state'] = 'selecting_point'
    return f"Select a point for {selected_char}:", get_point_keyboard(available_points)

def select_point(message, selected_point, selected_char, available_points):
    character = message.bot['character']
    character[selected_char] = selected_point
    character['points'][selected_char].remove(selected_point)
    message.bot['state'] = 'distributing_points'
    return f"{selected_point} points have been assigned to {selected_char}. Select another characteristic or type 'Done' to finish.", get_characteristic_keyboard(character['points'])

def go_back_to_characteristics(message):
    character = message.bot['character']
    message.bot['state'] = 'distributing_points'
    return "Select a characteristic to distribute points:", get_characteristic_keyboard(character['points'])

def finish_character_creation(message, characteristics):
    character = message.bot['character']
    if all(len(points) != 0 for points in character['points'].values()):
        message.bot['state'] = 'selecting_backstory_type'
        return "Тепеь, Выберете тип предыстории:", get_backstory_type_keyboard(backstory_types)
    else:
        return "Вы еще не закончили распределять очки персонажа", get_characteristic_keyboard(character['points'])

def select_backstory_type(message, selected_backstory_type):
    character = message.bot['character']
    character['backstory_type'] = selected_backstory_type
    message.bot['state'] = 'writing_backstory'
    return "Отличный выбор!Теперь напишите предысторию:"

def write_backstory(message, backstory):
    character = message.bot['character']
    character['backstory'] = backstory
    # Save the character to the database and get the character details
    character_details = save_character_to_db(character)
    # Construct the message with the character details
    character_info = f"Your character is {character_details['name']}\n\n"
    character_info += "Has the following characteristics:\n"
    for characteristic, value in character_details.items():
        if characteristic not in ['name', 'backstory', 'backstory_type']:
            character_info += f"{characteristic.capitalize()}: {value}\n"
    character_info += f"\nHas a backstory of type {character_details['backstory_type']}, with the following backstory:\n{character_details['backstory']}"
    # Send the character details to the user
    return character_info