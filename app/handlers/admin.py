from aiogram import types, Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.db_service import approve_recipe

router = Router()


@router.callback_query(F.data.startswith("act_"))
async def act_recipe_creation(call: types.CallbackQuery, session: AsyncSession):
    action: str = call.data.split("_")[1]
    recipe_id: int = int(call.data.split("_")[2])

    if action == "decline":
        await call.answer("Отклонен")
    else:
        await approve_recipe(session, recipe_id)
        await call.answer("Одобрен")

    await call.message.delete()
