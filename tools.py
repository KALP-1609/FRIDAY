def calculate(expression):
    return eval(expression)

def save_note(note):
    with open('notes.txt', 'a') as f:
        f.write(note + "\n")

    return "Note saved!"
