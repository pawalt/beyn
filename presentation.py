import re
import jinja2
from datetime import date
import os
import elems

def sanitize_title(title):
    """
    Transforms the input into a safe string for file naming.
    """
    filename = title.strip().replace(' ', '_')  # replacing spaces with underscores
    filename = re.sub(r'(?u)[^-\w.]', '', filename)  # removing all characters except alpha-numerics, dots, hyphens and underscores
    filename = filename.lower()  # convert filename to lowercase
    filename = filename[:250]
    return filename

recipe_template = """
+++
title = "{{ recipe.recipe_title }}"
description = "{{ recipe.description }}"
date = "{{ date }}"
total_time = "{{ recipe.total_time }}"
active_time = "{{ recipe.active_time }}"
+++

{% raw %}{{{% endraw %}< ai_recipe url="data/recipes/{{ filename }}" >{% raw %}}}{% endraw %}
""".strip()

hugo_base_dir = "/Users/peytonwalters/projects/personal-site"

def write_recipe_to_hugo(pathbase: str, recipe: elems.RecipeDetails):
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')

    json_filename = f"{pathbase}.json"

    content_template = jinja2.Template(recipe_template)
    content = content_template.render(
        recipe=recipe,
        filename=json_filename,
        date=formatted_date,
    )

    md_path = os.path.join(hugo_base_dir, "content", "recipes", f"ai_{pathbase}.md")
    json_path = os.path.join(hugo_base_dir, "data", "recipes", json_filename)

    with open(json_path, 'w') as f:
        f.write(recipe.json(indent=2))

    with open(md_path, 'w') as f:
        f.write(content)

machine_readable_recipe_format = """
Recipe Title: {{ recipe.recipe_title }}

Total time: {{ recipe.total_time }} minutes
Active time: {{ recipe.active_time }} minutes

Recipe Description: {{ recipe.description }}

Recipe Ingredients:
{% for item in recipe.ingredients -%}
- {{ item.quantity }} {{ item.unit }} {{ item.name }}
{% endfor %}
Recipe steps:
{% for step in recipe.steps -%}
- {{ step }}
{% endfor %}
""".strip()

def get_machine_format(recipe: elems.RecipeDetails):
    content_template = jinja2.Template(machine_readable_recipe_format)
    return content_template.render(
        recipe=recipe,
    )
