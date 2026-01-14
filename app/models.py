from sqlalchemy import Column, Integer, String, Text
from database import Base


class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title_dishes = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    ingridients_list = Column(Text, index=True)
    description = Column(Text, index=True)
    number_views = Column(Integer, index=True)
