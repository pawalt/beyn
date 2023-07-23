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

def write_recipe_to_hugo(recipe: elems.RecipeDetails):
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')

    sanitized_title = sanitize_title(recipe.recipe_title)
    json_filename = f"{sanitized_title}.json"

    content_template = jinja2.Template(recipe_template)
    content = content_template.render(
        recipe=recipe,
        filename=json_filename,
        date=formatted_date,
    )

    md_path = os.path.join(hugo_base_dir, "content", "recipes", f"ai_{sanitized_title}.md")
    json_path = os.path.join(hugo_base_dir, "data", "recipes", json_filename)

    with open(json_path, 'w') as f:
        f.write(recipe.json(indent=2))

    with open(md_path, 'w') as f:
        f.write(content)
