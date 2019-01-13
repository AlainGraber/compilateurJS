import ply.lex as lex

reserved_words = (
    'var',
    'console_log',
    'function',
    'while',
    'return',
    'true',
    'false',
)

tokens = (
             'COMMENT',
             'INC_OP',
             'NUMBER',
             'ADD_OP',
             'MUL_OP',
             'IDENTIFIER',
             'COMPARISON',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();={},><'

def t_COMMENT(t):
    r'//.*'
    pass  # No return value. Token discarded

def t_INC_OP(t):
    r'\+\+|--'
    return t

def t_ADD_OP(t):
    r'[+-]'
    return t


def t_MUL_OP(t):
    r'[*/]'
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()

    # Removes only the last word if var is present
    t.value = t.value.split(' ')[-1]

    return t

def t_COMPARISON(t):
    r'[=!]=|[<>]=?'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex(debug=False)

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break

        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
