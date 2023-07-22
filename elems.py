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
    quantity: str = Field(..., description="quantity of ingredients, empty if none specified")

class RecipeDetails(OpenAISchema):
    """RecipeDetails are the details describing a recipe. Details are precise and
reflect the input from the user."""
    description: str = Field(..., description="description of recipe steps in approximately 200 characters")
    steps: List[str] = Field(..., description="""specific list of all steps in the recipe, in order.
If multiple steps can be combined into one, they will.""")
    recipe_title: str = Field(..., description="title of the recipe")
    ingredients: List[Ingredient] = Field(..., description="list of all ingredients in the recipe")

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
