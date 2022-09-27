import json
import os

def open_json(target_json):
    with open(target_json, 'r') as f:
        content = json.load(f)
    f.close()
    return content
    
def write_json(content, target_json):
    with open(target_json, 'w') as f:
        json.dump(content, f, indent=4)
    f.close()
    
def cls():
    os.system('cls')