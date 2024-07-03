from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, Message, \
    CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.constants import BUTTONS
from app.keyboards import approve_keyboard, rate_keyboard
from app.service.db.models import Recipe
from app.service.db_service import get_recipes, add_recipe, add_rate_recipe
from app.service.pattern_analyzer import analyze_recipe
from app.settings import INLINE_QUERY_CACHE_TIME

router = Router()


@router.message(StateFilter("user:recipe"))
async def add_recipe_handler(message: Message, state: FSMContext, session: AsyncSession):
    unparsed_msg = await analyze_recipe(message)

    if isinstance(unparsed_msg, list):
        return await message.answer("\n".join(unparsed_msg))

    recipe_id: int = await add_recipe(session, unparsed_msg)

    await message.send_copy(
        chat_id=settings.ADMIN_ID,
        reply_markup=approve_keyboard(recipe_id)
    )

    await state.clear()


@router.inline_query(F.query == "recipes")
async def show_all_receipts(inline_query: InlineQuery, session: AsyncSession):

    def get_iq_text(recipe: Recipe) -> str:
        return (
            f'👨‍🍳 Рецепт №{recipe.id}\n'
            f'👍: {recipe.likes_count or 0}\n'
            f'👎: {recipe.dislikes_count or 0}\n\n'
            f'<b>{recipe.title}</b>\n\n'
            f'{recipe.description}'
        )

    results: list = []
    for recipe in await get_recipes(session):
        results.append(InlineQueryResultArticle(
            id=str(recipe.id),
            title=recipe.title,
            description=f"👍: {recipe.likes_count}\n" + recipe.description,
            thumbnail_url=recipe.media_uri,
            input_message_content=InputTextMessageContent(
                message_text=get_iq_text(recipe) + (f"<a href='{recipe.media_uri}'> Фото</a>" if recipe.media_uri else ""),
            ),
            reply_markup=rate_keyboard(recipe.id),
        ))
    if not results:
        results.append(InlineQueryResultArticle(
            id='1',
            title='Рецептов пока нет, добавить',
            description='Нажмите для добавления рецепта',
            input_message_content=InputTextMessageContent(
                message_text=BUTTONS['add_recipe']
            )
        ))

    await inline_query.answer(
        results=results,
        cache_time=INLINE_QUERY_CACHE_TIME,
    )


@router.callback_query(F.data.startswith('rate_'))
async def rate_recipe_handler(call: CallbackQuery, session: AsyncSession):
    data = call.data.split("_")
    action, recipe_id = data[1], int(data[2])

    await add_rate_recipe(session, recipe_id, action)

    await call.answer('Спасибо за отзыв!')

    await call.bot.edit_message_reply_markup(
        inline_message_id=call.inline_message_id,
        reply_markup=None,
    )


@router.message(F.text.startswith('👨‍🍳 Рецепт №'))
async def process_inline_message_recipe(message: Message):
    print(message)


"""
        await inline_query.bot.send_message(
            chat_id=inline_query.from_user.id,
            text='Оценте рецепт, это поможет другим!',
            reply_markup=rate_keyboard(),
        )
        """
