import random
import string
import re

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def is_valid_url(url):
    regex = re.compile(
        r'^(https?:\/\/)?'                  
        r'([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})?)'  
        r'(\/[^\s]*)?$'
    )
    return re.match(regex, url) is not None

def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url