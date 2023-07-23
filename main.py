import listen
import elems
import openai
from whispercpp import Whisper
from dotenv import load_dotenv
import os
import presentation

load_dotenv()
 
listen.record_audio()

w = Whisper.from_pretrained("small.en")

# transcription = w.transcribe_from_file(listen.RECORDING_FILE)
transcription = "Boil a medium large pot of water and salt it with two tablespoons of salt and a splash of olive oil. Take a pound of ground turkey and add two tablespoons of Worcestershire, ground onion, ground garlic, basil oregano, salt, and a little bit of salt. And then to take and then salt and pepper and panko breadcrumbs about a quarter cup and an egg, an entire egg. Mix the meat with the seasonings and form into balls that are in inch diameter. Bake the meatballs and place them on a cookie sheet and bake them at 350 degrees in an oven for about 20 minutes. While the meatballs are baking, add two cups of spaghetti to the boiling water and cook according to package instructions. Once meatballs are cooked, place in pot with tomato sauce, jarred tomato sauce. And then finally place the meatballs in the sauce over the pasta and add parmesan cheese."
print(transcription)

openai.api_key = os.getenv("OPENAI_API_KEY")

recipe = elems.get_completion("RecipeDetails", elems.RecipeDetails, transcription)

print(f"How to make {recipe.recipe_title}")

print("")

print(recipe.description)

print("")
print("Ingredients:")
for ingredient in recipe.ingredients:
    print(f"- {ingredient.quantity} {ingredient.unit} {ingredient.name}")

print("")
print("Recipe:")
for i, step in enumerate(recipe.steps):
    print(f"{i+1}. {step}")

presentation.write_recipe_to_hugo(recipe)

print(f"Wrote recipe")
