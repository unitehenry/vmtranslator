import sys
import os
from Parser import parse_tokens
from CodeWriter import translate

def get_filename(file_path):
    return file_path.split('/').pop().split('.vm')[0]

def get_output_path(filename):
    if os.path.isdir(sys.argv[1]):
        path = sys.argv[1].split('/')
        path.append(f'{filename}.asm')
        return '/'.join(path)
    else:
        path = sys.argv[1].split('/')
        path[len(path) - 1] = f'{filename}.asm'
        return '/'.join(path)

def get_instructions_for_file(path_to_file):
    with open(path_to_file, 'r') as input_file:
        filename = get_filename(path_to_file)
        tokens = parse_tokens(input_file.read())
        return translate(tokens, filename)

def main():

    instructions = []
    if os.path.isdir(sys.argv[1]):
        for filename in os.listdir(sys.argv[1]):
            if not '.vm' in filename: continue
            instructions.extend(get_instructions_for_file(f'{sys.argv[1]}/{filename}'))
    else:
        instructions.extend(get_instructions_for_file(sys.argv[1]))

    filename = get_filename(sys.argv[1])
    output_path = get_output_path(filename)
    with open(output_path, 'w') as output_file:
        output_file.write('\n'.join(instructions))
        output_file.close()

main()
