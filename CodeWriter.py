import sys

def init_instruction_counters():
    return {
        'EQ': 0,
        'GT': 0,
        'LT': 0
    }

def is_arithematic(token):
    return token in [
        'add', 'sub', 'neg',
        'eq', 'gt', 'lt',
        'and', 'or', 'not'
    ]

def is_memory_access(token):
    return ('pop' in token) or ('push' in token)

def is_branching(token):
    for command in [ 'label', 'goto', 'if-goto' ]:
        if command in token:
            return True
    return False

def get_arithematic_instuctions(token, counters):
    if token == 'add':
        return [
            '@SP', 'A=M', 'A=A-1', 'A=A-1',
            'D=M', 'A=A+1', 'D=D+M', 'A=A-1',
            'M=D', 'D=A', '@SP', 'M=D+1'
        ]
    if token == 'sub':
        return [
            '@SP', 'A=M', 'A=A-1', 'A=A-1',
            'D=M', 'A=A+1', 'D=D-M', 'A=A-1',
            'M=D', 'D=A', '@SP', 'M=D+1'
        ]
    if token == 'neg':
        return [ '@SP', 'A=M', 'A=A-1', 'M=-M' ]
    if token == 'eq':
        counters['EQ'] += 1
        eq_token = f'EQ{counters["EQ"]}'
        return [
            '@SP', 'A=M-1', 'A=A-1', 'D=M', '@R13', 'M=D', # Load M[SP - 2] -> R13
            '@SP', 'A=M-1', 'D=M', '@R14', 'M=D', # Load M[SP - 1] -> R14
            f'@{eq_token}', 'D=A', '@R15', 'M=D', '@EQ', '0;JMP', f'({eq_token})' # @EQx -> R15
        ]
    if token == 'gt':
        counters['GT'] += 1
        gt_token = f'GT{counters["GT"]}'
        return [
            '@SP', 'A=M-1', 'A=A-1', 'D=M', '@R13', 'M=D', # Load M[SP - 2] -> R13
            '@SP', 'A=M-1', 'D=M', '@R14', 'M=D', # Load M[SP - 1] -> R14
            f'@{gt_token}', 'D=A', '@R15', 'M=D', '@GT', '0;JMP', f'({gt_token})' # @GTx -> R15
        ]
    if token == 'lt':
        counters['LT'] += 1
        lt_token = f'LT{counters["LT"]}'
        return [
            '@SP', 'A=M-1', 'A=A-1', 'D=M', '@R13', 'M=D', # Load M[SP - 2] -> R13
            '@SP', 'A=M-1', 'D=M', '@R14', 'M=D', # Load M[SP - 1] -> R14
            f'@{lt_token}', 'D=A', '@R15', 'M=D', '@LT', '0;JMP', f'({lt_token})' # @LTx -> R15
        ]
    if token == 'and':
        return [
            '@SP', 'A=M-1', 'A=A-1', 'D=M',
            'A=A+1', 'D=D&M', 'A=A-1', 'M=D',
            'D=A', '@SP', 'M=D+1'
        ]
    if token == 'or':
        return [
            '@SP', 'A=M-1', 'A=A-1', 'D=M',
            'A=A+1', 'D=D|M', 'A=A-1', 'M=D',
            'D=A', '@SP', 'M=D+1'
        ]
    if token == 'not':
        return [ '@SP', 'A=M', 'A=A-1', 'M=!M' ]
    raise ValueError('Invalid arithematic instruction')

def push_from_segment(segment, offset):
    return [
        f'@{offset}', 'D=A', f'@{segment}', 'A=D+M', 'D=M',
        '@SP', 'A=M', 'M=D', 'D=A+1', '@SP', 'M=D'
    ]

def pop_from_segment(segment, offset):
    return [
        f'@{offset}', 'D=A', f'@{segment}', 'A=D+M', 'D=A', '@R13', 'M=D',
        '@SP', 'A=M-1', 'D=M', '@R13', 'A=M', 'M=D',
        '@SP', 'A=M-1', 'D=A', '@SP', 'M=D'
    ]

def get_memory_access_instructions(token, filename):
    if 'pop' in token:
        if 'local' in token:
            off = token.split('local').pop().strip()
            return pop_from_segment('LCL', off)
        if 'argument' in token:
            off = token.split('argument').pop().strip()
            return pop_from_segment('ARG', off)
        if 'this' in token:
            off = token.split('this').pop().strip()
            return pop_from_segment('THIS', off)
        if 'that' in token:
            off = token.split('that').pop().strip()
            return pop_from_segment('THAT', off)
        if 'static' in token:
            static = token.split('static').pop().strip()
            ref = filename
            return [
                '@SP', 'A=M-1', 'D=M', f'@{ref}.{static}', 'M=D',
                '@SP', 'M=M-1'
            ]
        if 'temp' in token:
            temp = token.split('temp').pop().strip()
            addr = 5 + int(temp)
            return [
                '@SP', 'A=M-1', 'D=M', f'@{addr}', 'M=D',
                '@SP', 'M=M-1'
            ]
        if 'pointer' in token:
            pointer = token.split('pointer').pop().strip()
            addr = 'THIS' if pointer == '0' else 'THAT'
            return [ '@SP', 'A=M-1', 'D=M', f'@{addr}', 'M=D', '@SP', 'M=M-1' ]
    if 'push' in token:
        if 'local' in token:
            off = token.split('local').pop().strip()
            return push_from_segment('LCL', off)
        if 'argument' in token:
            off = token.split('argument').pop().strip()
            return push_from_segment('ARG', off)
        if 'this' in token:
            off = token.split('this').pop().strip()
            return push_from_segment('THIS', off)
        if 'that' in token:
            off = token.split('that').pop().strip()
            return push_from_segment('THAT', off)
        if 'constant' in token:
            const = token.split('constant').pop().strip()
            return [ f'@{const}', 'D=A', '@SP', 'A=M', 'M=D', 'D=A+1', '@SP', 'M=D' ]
        if 'static' in token:
            static = token.split('static').pop().strip()
            ref = filename
            return [ f'@{ref}.{static}', 'D=M', '@SP', 'A=M', 'M=D', 'D=A+1', '@SP', 'M=D' ]
        if 'temp' in token:
            temp = token.split('temp').pop().strip()
            addr = 5 + int(temp)
            return [ f'@{addr}', 'D=M', '@SP', 'A=M', 'M=D', 'D=A+1', '@SP', 'M=D' ]
        if 'pointer' in token:
            pointer = token.split('pointer').pop().strip()
            addr = 'THIS' if pointer == '0' else 'THAT'
            return [ f'@{addr}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1' ]
    raise ValueError('Invalid memory access instruction')

def get_end_instruction():
    return [ '(END)', '@END', '0;JMP' ]

def get_eq_instruction():
    return [
        '(EQ)', '@R13', 'D=M', '@R14', 'D=D-M', '@IS_EQ', 'D;JEQ', '@NOT_EQ', '0;JMP',
        '(NOT_EQ)', '@SP', 'A=M-1', 'A=A-1', 'M=0', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP',
        '(IS_EQ)', '@SP', 'A=M-1', 'A=A-1', 'M=-1', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP'
    ]

def get_gt_instruction():
    return [
        '(GT)', '@R13', 'D=M', '@R14', 'D=D-M', '@IS_GT', 'D;JGT', '@NOT_GT', '0;JMP',
        '(NOT_GT)', '@SP', 'A=M-1', 'A=A-1', 'M=0', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP',
        '(IS_GT)', '@SP', 'A=M-1', 'A=A-1', 'M=-1', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP'
    ]

def get_lt_instruction():
    return [
        '(LT)', '@R13', 'D=M', '@R14', 'D=D-M', '@IS_LT', 'D;JLT', '@NOT_LT', '0;JMP',
        '(NOT_LT)', '@SP', 'A=M-1', 'A=A-1', 'M=0', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP',
        '(IS_LT)', '@SP', 'A=M-1', 'A=A-1', 'M=-1', 'D=A+1', '@SP', 'M=D', '@R15', 'A=M', '0;JMP'
    ]

def get_branching_instructions(token):
    if 'label' in token:
        label = token.split('label').pop().strip()
        return [ f'({label})' ]
    if 'if-goto' in token:
        label = token.split('if-goto').pop().strip()
        return [ '@SP', 'A=M-1', 'D=M', '@SP', 'M=M-1', f'@{label}', 'D;JNE' ]
    if 'goto' in token:
        label = token.split('goto').pop().strip()
        return [ f'@{label}', '0;JMP' ]
    raise ValueError('Invalid branching instruction')

def translate(tokens, filename):
    instructions = []
    counters = init_instruction_counters()
    for token in tokens:
        if is_arithematic(token):
            for instruction in get_arithematic_instuctions(token, counters):
                instructions.append(instruction)
        if is_memory_access(token):
            for instruction in get_memory_access_instructions(token, filename):
                instructions.append(instruction)
        if is_branching(token):
            for instruction in get_branching_instructions(token):
                instructions.append(instruction)
    instructions.extend(get_end_instruction())
    instructions.extend(get_eq_instruction())
    instructions.extend(get_gt_instruction())
    instructions.extend(get_lt_instruction())
    return instructions
