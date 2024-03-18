import sys
from Parser import parse_tokens
from CodeWriter import translate

def get_filename():
    return sys.argv[1].split('/').pop().split('.vm')[0]

def get_output_path(filename):
    path = sys.argv[1].split('/')
    path[len(path) - 1] = f'{filename}.asm'
    return '/'.join(path)

def main():
    instuctions = []
    with open(sys.argv[1], 'r') as input_file:
        filename = get_filename()
        tokens = parse_tokens(input_file.read())
        instructions = translate(tokens, filename)
    output_path = get_output_path(filename)
    with open(output_path, 'w') as output_file:
        output_file.write('\n'.join(instructions))
        output_file.close()

main()
