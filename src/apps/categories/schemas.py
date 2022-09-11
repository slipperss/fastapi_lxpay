from tortoise.contrib.pydantic import pydantic_model_creator

from src.apps.categories.models import Category


CategoryIn = pydantic_model_creator(
    Category,
    name='CategoryIn',
    exclude_readonly=True,
)

CategoryOut = pydantic_model_creator(
    Category,
    name='CategoryOut',
)
