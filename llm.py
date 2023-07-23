import elems
import presentation

import openai
from openai_function_call import OpenAISchema

GPT_3 = "gpt-3.5-turbo-0613"
GPT_4 = "gpt-4-0613"

def get_shema_obj(name: str, md: OpenAISchema, transcript: str):
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

def make_modifications(modification: str, recipe: elems.RecipeDetails) -> str:
    machine_readable = presentation.get_machine_format(recipe)

    completion = openai.ChatCompletion.create(
            model=GPT_3,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert recipe developer who follows instructions
to a tee and knows everything about recipe development. Do not ask any questions. Only respond in
full recipes.""",
                },
                {
                    "role": "user",
                    "content": f"I want you to make modifications to the following recipe. The instructions for modification are: {modification}",
                },
                {
                    "role": "user",
                    "content": machine_readable,
                },
            ],
        )
    
    return completion.choices[0].message.content
