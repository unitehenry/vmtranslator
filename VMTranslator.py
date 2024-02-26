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
    file = open(sys.argv[1], 'r')
    filename = get_filename()
    tokens = parse_tokens(file.read())
    instructions = translate(tokens, filename)
    output_path = get_output_path(filename)
    output = open(output_path, 'a')
    output.write('\n'.join(instructions))
    output.close()

main()
