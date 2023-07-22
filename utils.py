import re

def title_to_filename(title):
    """
    Transforms the input into a safe string for file naming.
    """
    filename = title.strip().replace(' ', '_')  # replacing spaces with underscores
    filename = re.sub(r'(?u)[^-\w.]', '', filename)  # removing all characters except alpha-numerics, dots, hyphens and underscores
    filename = filename.lower()  # convert filename to lowercase
    filename = filename[:250] + '.json'  # append .json at the end, ensure the total length is under 255
    return filename