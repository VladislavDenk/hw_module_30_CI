from typing import Annotated, Optional

from pydantic import BaseModel, Field, PositiveInt


class BaseRecipe(BaseModel):

    title_dishes: str
    cooking_time: PositiveInt
    ingredients_list: str
    description: Optional[str]
    number_views: Annotated[int, Field(ge=0)] = 0


class RecipeSchema(BaseRecipe):
    id: int

    class Config:
        orm_mode = True
