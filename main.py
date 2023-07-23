import listen
import elems
import openai
from whispercpp import Whisper
from dotenv import load_dotenv
import os
import presentation
import llm

load_dotenv()

def get_voice_input(whisp: Whisper) -> str:
    listen.record_audio()
    return whisp.transcribe_from_file(listen.RECORDING_FILE)

def parse_recipe(source: str) -> elems.RecipeDetails:
    return llm.get_shema_obj("RecipeDetails", elems.RecipeDetails, source)

w = Whisper.from_pretrained("small.en")

# transcription = get_voice_input(w)
transcription = "So I'm gonna give a recipe for quesadillas. First thing you gotta do is you gotta get out a spice blend. I usually use like cumin oregano and chili flakes. Put that in a mortar and pestle and grind it up. Probably, I don't know. Just like four to... Sorry. Two to one to one, cumin to oregano to chili flakes. Grind that up into a powder. Add in some garlic. Grind that up into a paste in the mortar and pestle. Combine it with mayo. Not a whole lot. Just a bit. I would say maybe half a cup of mayo. Then take six boneless skinless chicken thighs. Marinate the boneless skinless chicken thighs in the mayo. Then sear them off on a cast iron grill. More cast iron skillet, actually. Once they're seared off, I normally do them to 155 degrees Fahrenheit internal. Once they're seared off, I chop them up. Combine them with a few cups of shredded cheese. Anything will do, but pepper jack is great. Mix that up. On the side, you can do some caramelized onions. Add the caramelized onions in. Mix up the cheese, chicken, and the caramelized onions. Actually, the chicken should be diced, not sliced. Mix it all up. Pack it inside of tortillas. You want to just fold the tortilla on the mixture. Stir the tortilla off on the griddle and give it a minute to cool off. Cut them up into quarters and serve them along with some hot sauce. I like to use green chalula."
print(transcription)

openai.api_key = os.getenv("OPENAI_API_KEY")

recipe = parse_recipe(transcription)
pathbase = presentation.sanitize_title(recipe.recipe_title)

presentation.write_recipe_to_hugo(pathbase, recipe)

print(presentation.get_machine_format(recipe))

while True:
    choice = input("would you like to modify (y/n) ")
    choice = choice.strip()
    choice = choice.lstrip('q')
    print(choice)
    if choice != "y":
        break

    "What modifications would you like to make?"
    modifications = get_voice_input(w)
    print(modifications)

    new_recipe = llm.make_modifications(modifications, recipe)
    print(new_recipe)

    recipe = parse_recipe(new_recipe)
    presentation.write_recipe_to_hugo(pathbase, recipe)
