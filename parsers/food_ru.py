import asyncio
from typing import List

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.service.content_cdn.YasoSu import yasosu__paste
from app.service.db.models import Recipe

import requests

from app.settings import DATABASE_URL

URL__GET_RECIPES_LIST: str = 'https://api.food.ru/content/recipes?format=json&max_per_page={}&page={}'
URL__GET_RECIPE_INFO: str = 'https://api.food.ru/content/v2/recipes/{}?preview=false&format=json'


def foodru__get_recipes(total_limit: int) -> List[int]:
    result: List[int] = []

    limit = 20
    page = 1

    while len(result) < total_limit:
        r = requests.get(URL__GET_RECIPES_LIST.format(limit, page))

        result.extend([val['id'] for val in r.json()['materials']])

    return result[:total_limit]


def foodru__get_recipe_info(recipe_id: int) -> dict:
    r = requests.get(URL__GET_RECIPE_INFO.format(recipe_id))

    resp_json: dict = r.json()

    title = resp_json['title']

    ingredients: str = "Ингредиенты:\n" + "\n".join(
        [
            val['title'] + ": " + str(val['custom_measure_count']) + ' ' + val['custom_measure']
            for val in resp_json['main_ingredients']
        ]
    )

    allergens: str = "\n\nАллергены: " + (resp_json['allergens'] or 'Отсутсвуют')

    return {
        "title": title,
        "description": ingredients + allergens + "\n" + foodru__get_steps_to_cook(resp_json['cooking']),
    }


def foodru__get_steps_to_cook(data: List[dict]) -> str:
    res: List[str] = []
    for step_info in data:
        step_title: str = step_info['title']
        step_content: str = step_info['description']['children'][0]['children'][0]['content']

        res.append(step_title + "\n" + step_content)

    return yasosu__paste("\n\n".join(res))


async def main():

    for recipe_id in foodru__get_recipes(20):
        info = foodru__get_recipe_info(recipe_id)

        stmt = insert(Recipe).values(
            title=info['title'],
            description=info['description'],
            user=1888872438,
            approved=True,
        )

        engine = create_async_engine(DATABASE_URL, echo=False)
        session = async_sessionmaker(bind=engine)

        async with session() as session:
            await session.execute(stmt)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
