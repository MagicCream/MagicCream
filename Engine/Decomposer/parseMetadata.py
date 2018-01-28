from ply import lex, yacc
#from services import Argument

# Lexer
# TODO metadata
# TODO cache

tokens = (
    "PREFIX",
    "URI",
    "SEPARATOR",
    "POINT"
)
PREFIX_NOTATION = "@prefix"

t_PREFIX = r"[a-z](\S)*(?=: )"
t_URI = r"<"+"\S+"+r">"
t_SEPARATOR = r":"
t_POINT = r"\."

t_ignore = ' \t\n\r'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex(debug=1)

# Parser

def p_prefix_uri_list_1(p):
    """
    prefix_uri_list : prefix_uri prefix_uri_list
    """
    p[1].update(p[2])
    p[0] = p[1]

def p_prefix_uri_list_2(p):
    """
    prefix_uri_list : prefix_uri
    """
    p[0] = p[1]

def p_prefix_uri(p):
    """
    prefix_uri : PREFIX SEPARATOR URI POINT
    """
    p[0] = {p[1]:p[3]}

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=1)

# Helpers

def parse(file):
    meta_data = ""
    for line in file.readlines():
        if line.startswith(PREFIX_NOTATION):
            meta_data += line[8:]
        else :
            break
    rlt = parser.parse(meta_data, lexer=lexer)
    return rlt
