from typing import List

from sqlalchemy import select, ScalarResult, insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.db.models import Recipe, User


async def get_recipes(
        session: AsyncSession, limit: int = 50, offset: int = 0, approved: bool = True
) -> ScalarResult[Recipe]:
    """получение рецептов из БД"""
    res = await session.execute(select(Recipe).limit(limit).offset(offset).where(Recipe.approved == approved))
    return res.scalars()


async def add_recipe(session: AsyncSession, data: dict) -> int:
    """
    создание рецепта

    :return: recipe id in database
    """
    res = await session.execute(insert(Recipe).values(**data))
    pk_ = res.inserted_primary_key[0]

    await session.commit()
    return pk_


async def add_rate_recipe(
        session: AsyncSession, recipe_id: int, type_: str = 'like'
) -> None:
    """инкремент лайка/дизлайка"""
    vals = {'likes_count' if type_ == 'like' else 'dislikes_count': Recipe.likes_count + 1}

    await session.execute(
        update(Recipe)
        .values(**vals)
        .where(Recipe.id == recipe_id)
    )
    await session.commit()


async def approve_recipe(session: AsyncSession, recipe_id: int) -> None:
    print(recipe_id)
    stmt = update(Recipe).values(approved=True).where(Recipe.id == recipe_id)
    await session.execute(stmt)
    await session.commit()


async def add_user(session: AsyncSession, user_id: int) -> None:
    """регистрация пользователя в БД"""
    try:
        await session.execute(insert(User).values(id=user_id))
        await session.commit()
    except IntegrityError:
        pass


