import openai
from openai_function_call import OpenAISchema

from pydantic import Field, BaseModel
from typing import List

GPT_3 = "gpt-3.5-turbo-0613"
GPT_4 = "gpt-4-0613"

class Ingredient(BaseModel):
    """Ingredient in the recipe. Do not enter anything for fields not specified by the user."""
    name: str = Field(..., description="Ingredient name")
    unit: str = Field(..., description="abbreviated unit name in standard form, empty if none specified")
    quantity: str = Field(..., description="enter -1 if no quantity is specified")

class Ingredients(OpenAISchema):
    """Ingredients is a list of all ingredients from the provided recipe."""
    ingredients: List[Ingredient] = Field(..., description="list of all ingredients in the recipe")

class Title(OpenAISchema):
    """Title is the assistant-generated title of the provided recipe."""
    recipe_title: str = Field(..., description="title of the recipe")

class Steps(OpenAISchema):
    """Steps provided in the recipe. Steps are provided in-order and are very specific. 
    If multiple steps can be combined into one easily, they will."""
    steps: List[str] = Field(..., description="list of all steps in the recipe, in order")

class Description(OpenAISchema):
    """Description of recipe in less than 100 characters"""
    description: str = Field(..., description="description of recipe")

def get_completion(name: str, md: OpenAISchema, transcript: str):
    completion = openai.ChatCompletion.create(
            model=GPT_3,
            temperature=0.7,
            functions=[md.openai_schema],
            messages=[
                {
                    "role": "system",
                    "content": f"The user wants information about {name}. Use {name} to parse this info.",
                },
                {
                    "role": "user",
                    "content": transcript,
                },
            ],
        )
    ingreds = md.from_response(completion)
    return ingreds

