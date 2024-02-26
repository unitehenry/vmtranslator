def parse_tokens(content):
    tokens = []
    for line in content.split('\n'):
        line_string = line.strip()
        if not line_string: continue
        if '//' in line_string and line_string.index('//') == 0: continue
        tokens.append(line_string)
    return tokens
