import os
import json

def jsonify():
    current_path = "\\".join(os.path.abspath(__file__).split('\\')[:-2])
    file_name = "config.json"
    path_json = os.path.join(current_path, file_name)
    with open(path_json) as jsonfile:
        return json.load(jsonfile)
    
