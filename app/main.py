import logging
from typing import Annotated
from contextlib import asynccontextmanager


import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import select, update, desc, asc

import models
import schemas
from database import get_session, AsyncSession, engine

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TABLE = models.RecipeModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Процесс создания таблицы...")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Таблица успешно создана")
    yield
    logger.info("Закрытие соединения")
    await engine.dispose()
    logger.info("Соединение закрыто")


app = FastAPI(lifespan=lifespan)


@app.post("/recipes", summary="Добавление нового рецепта", tags=["Рецепты"])
async def add_recipes(data: schemas.BaseRecipe, session: SessionDep):
    new_recipe = TABLE(
        title_dishes=data.title_dishes,
        cooking_time=data.cooking_time,
        ingridients_list=data.ingredients_list,
        description=data.description,
        number_views=data.number_views,
    )
    session.add(new_recipe)
    await session.commit()
    

    return {"status": "Рецепт успешно добавлен"}


@app.get("/recipes", summary="Получить все рецепты", tags=["Рецепты"])
async def get_recipes(session: SessionDep):
    query = select(TABLE).order_by(desc(TABLE.number_views), asc(TABLE.cooking_time))
    result = await session.execute(query)
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", summary="Получить все рецепты", tags=["Рецепты"])
async def get_recipes_by_id(recipe_id: int, session: SessionDep):
    req = select((TABLE)).where(TABLE.id == recipe_id)
    new_session = await session.execute(req)
    result = new_session.scalars().first()

    request = select((TABLE.number_views)).where(TABLE.id == recipe_id)
    new_session = await session.execute(request)
    number_view = new_session.scalars().one()
    new_number_view = number_view + 1

    update_view_number = (
        update(TABLE).where(TABLE.id == recipe_id).values(number_views=new_number_view)
    )
    await session.execute(update_view_number)
    await session.commit()

    return result


if __name__ == "__main__":
    print("Запуск приложения")
    uvicorn.run('main:app', reload=True)