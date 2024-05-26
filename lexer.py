import re

# トークンの定義
tokens = [
    ('GROUP_KEYWORD', r'public\s+group'),
    ('FUNC_KEYWORD', r'public\s+func'),
    ('RUNNER_KEYWORD', r'public\s+runner'),
    ('IDENTIFIER', r'[\u4e00-\u9fff_a-zA-Z][\u4e00-\u9fff_a-zA-Z0-9]*'),
    ('LEFT_BRACE', r'{'),
    ('RIGHT_BRACE', r'}'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('HASH', r'#'),
    ('EQUALS', r'='),
    ('SEMICOLON', r';'),
    ('DOT', r'\.'),
    ('COMMA', r','),
    ('STRING', r'\".*?\"'),
    ('COMMENT', r'\/\/.*'),
    ('ADD', r'\+'),
    ('SUBTRACT', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('NUMBER', r'\d+'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+')
]

# 正規表現パターンの結合
pattern = '|'.join('(?P<%s>%s)' % pair for pair in tokens)

# Lexer
def lexer(code):
    pos = 0
    lineno = 1

    while pos < len(code):
        match = re.match(pattern, code[pos:])
        if not match:
            raise SyntaxError(f"Invalid token at line {lineno}")

        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == 'NEWLINE':
            lineno += 1
        elif token_type != 'WHITESPACE' and token_type != 'COMMENT':
            yield token_type, token_value

        pos += len(match.group(0))