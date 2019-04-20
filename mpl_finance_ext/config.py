import json
import os

PATH = os.path.dirname(__file__)

config = open(PATH + '/config.json').read()
config = json.loads(config)
