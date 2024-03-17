def parse_tokens(content):
    tokens = []
    for line in content.split('\n'):
        line_string = line.strip()
        if not line_string: continue
        if '//' in line_string and line_string.index('//') == 0: continue
        if '//' in line_string and line_string.index('//') != 0:
            line_string = line.split('//')[0].strip()
        tokens.append(line_string)
    return tokens
