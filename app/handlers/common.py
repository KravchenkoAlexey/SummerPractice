from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import BUTTONS
from app.keyboards import main_keyboard, search_recipes_keyboard
from app.service.db_service import add_user

router = Router()


@router.message(Command('start'), StateFilter("*"))
async def send_welcome(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    await add_user(session, message.chat.id)

    await message.answer(
        "Добро пожаловать в Кулинарочку. Выберите действие из меню ниже.", reply_markup=main_keyboard()
    )


@router.message(F.text == BUTTONS['show_recipes'])
async def show_recipes_menu(message: types.Message):
    await message.answer(
        "Нажмите кнопку ниже для просмотра рецептов, имеющихся в базе бота.", reply_markup=search_recipes_keyboard()
    )


@router.message(F.text == BUTTONS['add_recipe'])
async def add_recipe_init(message: types.Message, state: FSMContext):
    await message.answer(
        """
Пришлите ваш рецепт одним сообщением, вы можете прикрепить к сообщению фотографию.
<b>Строго придерживайтесь формата из примера ниже!</b>

<i>Если рецепт длинный и требует инструкции с фото, вы можете добавить в Ваше сообщение ссылку на ресурс (например: telegra.ph),
в котором поместите всю необходимую информацию.</i>

Пример:
Панкейки (американские блинчики)

Продукты (на 4 порции):
- Яйца - 2 шт.
- Молоко - 200 мл
- Мука пшеничная - 10 ст. л.
- Разрыхлитель - 1 ч. л.
- Сахар - 2 ст. л.
- Ванильный сахар (по желанию) - по вкусу

Вот все ингредиенты, которые нам понадобятся. С указанным количеством сахара (30 г), панкейки получаются не очень сладкие, подойдут и для тех, кто ест их со сладкими добавками, и для тех, кто предпочитает несладкие (например со сметаной или сыром). Но всё же, если вы любите послаще, добавьте ещё сахара. Также можно экспериментировать со вкусами и добавить, например, ванильный сахар или корицу.


<i>P.S. Первая строка рецепта - название - обязательно!</i>
"""
    )
    await state.set_state("user:recipe")

