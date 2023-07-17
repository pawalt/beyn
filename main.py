import listen
import llm
import elems
import openai
from whispercpp import Whisper
from dotenv import load_dotenv
import os

load_dotenv()
 
listen.record_audio()

w = Whisper.from_pretrained("small.en")

# transcription = w.transcribe_from_file(listen.RECORDING_FILE)
transcription = """
Alright, so in order to make quesadilla, you have to start with one tortilla. You have to start with one boneless skinless chicken thigh. But before any of that, you should take two cloves of garlic, put them in a mortar and pestle, and smash them up with salt and pepper. Then add in some cayenne and add in some cumin. Mash that up until it's a paste. You're just going to do a sprinkle of both of those. Then combine the result from that mortar and pestle with some mayo. Then take that mayo and mortar and pestle marinade and marinade on to the boneless skinless chicken. Let that rest for about 30 minutes until the marinade incorporates. After that, you're going to sear it on a cast iron. Sear both sides until it's 150 internal. That's 150 Fahrenheit. And then after that, chop it up, throw it in a tortilla with cheese and caramelized onions. Make sure to mix all that up so that it's a homogenous mixture. Fold it up, put it back on the cast iron to sear it on both sides so it gets crunch. Pull it out. Set it on the cutting board. it up and eat it with some hot sauce.
How to make Quesadilla
"""
print(transcription)

openai.api_key = os.getenv("OPENAI_API_KEY")

title = elems.get_completion("Title", elems.Title, transcription)
ingredients = elems.get_completion("Ingredients", elems.Ingredients, transcription)
steps = elems.get_completion("Steps", elems.Steps, transcription)
description = elems.get_completion("Description", elems.Description, transcription)

print(f"How to make {title.recipe_title}")

print("")

print(description.description)

print("")
print("Ingredients:")
for ingredient in ingredients.ingredients:
    print(f"- {ingredient.quantity} {ingredient.unit} {ingredient.name}")

print("")
print("Recipe:")
for i, step in enumerate(steps.steps):
    print(f"{i+1}. {step}")
