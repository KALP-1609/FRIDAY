from memory import *

def calculate(expression):
    return eval(expression)

def save_note(note):
    with open('notes.txt', 'a') as f:
        f.write(note + "\n")

    return "Note saved!"

def remember(key,value):
    return save_memory(key=key,value=value)

def recall(key):
    result = get_memory(key=key)
    if result is None:
        return "No memory found!"
    return result
