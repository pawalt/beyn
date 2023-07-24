import listen
import elems
import openai
from whispercpp import Whisper
from dotenv import load_dotenv
import os
import presentation
import llm
import tempfile
import subprocess
import re
import json
from pydantic.tools import parse_obj_as

load_dotenv()

def get_voice_input(whisp: Whisper) -> str:
    listen.record_audio()
    return whisp.transcribe_from_file(listen.RECORDING_FILE)

def parse_recipe(source: str) -> elems.RecipeDetails:
    return llm.get_shema_obj("RecipeDetails", elems.RecipeDetails, source)

def get_vim_input(original: str):
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as temp:
        temp.write(original.encode())
        temp.flush()  # Ensure that the written data is flushed to disk
        temp_path = temp.name

    subprocess.call(['nvim', temp.name])

    with open(temp_path, 'r') as f:
        edited_content = f.read()

    return edited_content
   
def run_modification_repl(pathbase: str, recipe: elems.RecipeDetails):
    while True:
        choice = nice_input("would you like to do audio or vim input? (a/v/n) ")

        if choice == "a":
            "What modifications would you like to make?"
            modifications = get_voice_input(w)

            new_recipe = llm.make_modifications(modifications, recipe)
        elif choice == "v":
            original = presentation.get_machine_format(recipe)
            new_recipe = get_vim_input(original)
        else:
            break

        print(new_recipe)

        recipe = parse_recipe(new_recipe)
        presentation.write_recipe_to_hugo(pathbase, recipe)

def nice_input(prompt: str):
    choice = input(prompt)
    choice = choice.strip()
    choice = choice.lstrip('q')
    return choice
    
if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    w = Whisper.from_pretrained("small.en")

    choice = nice_input("would you like to create a new recipe or modify an existing one? (n/m): ")
    if choice == "n":
        # transcription = get_voice_input(w)
        transcription = "So I'm gonna give a recipe for quesadillas. First thing you gotta do is you gotta get out a spice blend. I usually use like cumin oregano and chili flakes. Put that in a mortar and pestle and grind it up. Probably, I don't know. Just like four to... Sorry. Two to one to one, cumin to oregano to chili flakes. Grind that up into a powder. Add in some garlic. Grind that up into a paste in the mortar and pestle. Combine it with mayo. Not a whole lot. Just a bit. I would say maybe half a cup of mayo. Then take six boneless skinless chicken thighs. Marinate the boneless skinless chicken thighs in the mayo. Then sear them off on a cast iron grill. More cast iron skillet, actually. Once they're seared off, I normally do them to 155 degrees Fahrenheit internal. Once they're seared off, I chop them up. Combine them with a few cups of shredded cheese. Anything will do, but pepper jack is great. Mix that up. On the side, you can do some caramelized onions. Add the caramelized onions in. Mix up the cheese, chicken, and the caramelized onions. Actually, the chicken should be diced, not sliced. Mix it all up. Pack it inside of tortillas. You want to just fold the tortilla on the mixture. Stir the tortilla off on the griddle and give it a minute to cool off. Cut them up into quarters and serve them along with some hot sauce. I like to use green chalula."
        print(transcription)
        recipe = parse_recipe(transcription)
        pathbase = presentation.sanitize_title(recipe.recipe_title)

        presentation.write_recipe_to_hugo(pathbase, recipe)

        print(presentation.get_machine_format(recipe))

        run_modification_repl(pathbase, recipe)
    elif choice == "m":
        url = nice_input("give the url for the recipe: ")
        # Regular expression pattern
        pattern = r'https?://[^/]+/recipes/ai_([^/]+)/?'

        # Use re.search to find matches
        match = re.search(pattern, url)

        if match:
            recipe_name = match.group(1)  # anything after 'recipes/' until the next '/'

            json_path = os.path.join(presentation.hugo_base_dir, "data", "recipes", f"{recipe_name}.json")
            with open(json_path, 'r') as f:
                file_contents = f.read()
            recipe_dict = json.loads(file_contents)

            recipe = parse_obj_as(elems.RecipeDetails, recipe_dict)
            run_modification_repl(recipe_name, recipe)
        else:
            print(f"it must be URL. Example:\nhttp://localhost:1313/recipes/ai_small_batch_granola/\nYours:\n{url}")

    else:
        print(f"idk what \"{choice}\" means")
