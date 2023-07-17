## Deprecated

import openai
from typing import List
import json

GPT_3 = "gpt-3.5-turbo-0613"
GPT_4 = "gpt-4-0613"

def get_ingredients(transcription: str) -> List[str]:
    completion = openai.ChatCompletion.create(
            model=GPT_3,
            temperature=0.7,
            functions=[{
                "name": "return_ingredients",
                "description": "Return a list of the ingredients from recipe",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ingredients": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                    },
                                    "unit": {
                                        "type": "string",
                                        "description": "abbreviated unit name, empty if none specified",
                                    },
                                    "quantity": {
                                        "type": "number",
                                        "description": "enter -1 if no quantity is specified",
                                    },
                                },
                            },
                            "description": "an array of all the ingredients in the recipe",
                        },
                    },
                    "required": ["ingredients"],
                },
            }],
            messages=[
                {
                    "role": "system",
                    "content": "Call the return_ingredients function with all the ingredients from the recipe the user tells you about.",
                },
                {
                    "role": "user",
                    "content": transcription,
                },
            ],
        )
    
    choice = completion["choices"][0]

    if choice["finish_reason"] != "function_call":
        print(f"expected finish reason function call but got {choice['finish_reason']}")
        return []
    
    args = choice["message"]["function_call"]["arguments"]

    return json.loads(args)["ingredients"]

def get_steps(transcription: str) -> List[str]:
    completion = openai.ChatCompletion.create(
            model=GPT_3,
            temperature=0.7,
            functions=[{
                "name": "return_steps",
                "description": "Return a list of steps required to complete the recipe",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            },
                            "description": "an array of all the steps in the recipe, in order",
                        },
                    },
                    "required": ["steps"],
                },
            }],
            messages=[
                {
                    "role": "system",
                    "content": "Call the return_steps function with all the required steps from the recipe the user tells you about.",
                },
                {
                    "role": "user",
                    "content": transcription,
                },
            ],
        )
    
    choice = completion["choices"][0]

    if choice["finish_reason"] != "function_call":
        print(f"expected finish reason function call but got {choice['finish_reason']}")
        return []
    
    args = choice["message"]["function_call"]["arguments"]

    return json.loads(args)["steps"]

def get_title(transcription: str) -> List[str]:
    completion = openai.ChatCompletion.create(
            model=GPT_3,
            temperature=0.7,
            functions=[{
                "name": "return_title",
                "description": "Return a title for the recipe",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "a title for the recipe",
                        },
                    },
                    "required": ["title"],
                },
            }],
            messages=[
                {
                    "role": "system",
                    "content": "Call the return_title function with a name for the recipe the user tells you about.",
                },
                {
                    "role": "user",
                    "content": transcription,
                },
            ],
        )
    
    choice = completion["choices"][0]

    if choice["finish_reason"] != "function_call":
        print(f"expected finish reason function call but got {choice['finish_reason']}")
        return []
    
    args = choice["message"]["function_call"]["arguments"]

    return json.loads(args)["title"]