import openai
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())

os.environ['OPENAI_API_KEY']= secrets['OPENAI_API_KEY']
