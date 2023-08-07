import listen
import time
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
import wave
import queue
import threading

load_dotenv()

def get_voice_input(whisp: Whisper) -> str:
    ch = queue.Queue()
    content_channel = queue.Queue()
    recorder = listen.Recorder()

    t = threading.Thread(target=listen.record_audio, args=(ch,recorder))
    worker_thread = threading.Thread(target=worker, args=(ch,content_channel, recorder, whisp))

    t.start()
    worker_thread.start()

    full_transcript = ""
    while True:
        transcript = content_channel.get()
        if transcript is None:
            break

        full_transcript += transcript
        print(transcript, end="", flush=True)

    print()

    t.join()
    worker_thread.join()

    return full_transcript

def worker(ch, content_channel, recorder, whisp: Whisper):
    while True:
        audio_slice = ch.get()
        if audio_slice is None:  # A sentinel value to exit the loop.
            content_channel.put(None)
            break

        fname = f"audiofiles/slice_{time.time()}.wav"

        with wave.open(fname, 'wb') as waveFile:
            waveFile.setnchannels(recorder.CHANNELS)
            waveFile.setsampwidth(recorder.audio.get_sample_size(recorder.FORMAT))
            waveFile.setframerate(recorder.RATE)
            waveFile.writeframes(audio_slice)

        transcript = whisp.transcribe_from_file(fname)
        
        content_channel.put(transcript)

        os.remove(fname)

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
        transcription = get_voice_input(w)

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
