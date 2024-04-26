import aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Create New Character"))
    keyboard.add(KeyboardButton("Edit Existing Character"))
    keyboard.add(KeyboardButton("View Existing Characters"))
    return keyboard

def get_class_keyboard(classes):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for class_name in classes:
        keyboard.add(KeyboardButton(class_name))
    return keyboard

def get_characteristic_keyboard(points):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for char, available_points in points.items():
        if available_points:
            keyboard.add(KeyboardButton(char))
    keyboard.add(KeyboardButton('Done'))
    return keyboard

def get_point_keyboard(available_points):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for point in available_points:
        keyboard.add(KeyboardButton(str(point)))
    keyboard.add(KeyboardButton('Back'))
    return keyboard

def get_backstory_type_keyboard(backstory_types):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for backstory_type in backstory_types:
        keyboard.add(KeyboardButton(backstory_type))
    return keyboard