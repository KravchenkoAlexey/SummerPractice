from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.constants import BUTTONS


def main_keyboard():
    builder = ReplyKeyboardBuilder()

    [builder.add(KeyboardButton(text=t)) for t in BUTTONS.values()]

    return builder.as_markup(resize_keyboard=True)


def search_recipes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Поиск', switch_inline_query_current_chat='recipes')
            ]
        ]
    )


def approve_keyboard(recipe_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅', callback_data=f'act_approve_{recipe_id}'),
                InlineKeyboardButton(text='🚫', callback_data=f'act_decline_{recipe_id}')
            ]
        ]
    )


def rate_keyboard(recipe_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='👍', callback_data=f'rate_like_{recipe_id}'),
                InlineKeyboardButton(text='👎', callback_data=f'rate_dislike_{recipe_id}')
            ]
        ]
    )
