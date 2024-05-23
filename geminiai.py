import pathlib
import textwrap
import yaml

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


config = yaml.safe_load(open("config.yaml"))
genai.configure(api_key=config['google']['api_key'])
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
response = model.generate_content("What is the meaning of life?")
to_markdown(response.text)