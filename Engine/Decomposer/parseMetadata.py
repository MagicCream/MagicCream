from ply import lex, yacc
#from services import Argument

# Lexer
# TODO metadata
# TODO cache

tokens = (
    "PREFIX",
    "URI",
    "POINT"
)
PREFIX_NOTATION = "@prefix"

t_PREFIX = r"[a-z](\S)*"+":"
t_URI = r"<"+"\S+"+r">"
t_POINT = r"\."

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex(debug=1)

# Parser

def p_prefix_uri(p):
    """
    prefix_uri : PREFIX URI POINT
    """
    p[0] = p[2]

def p_prefix_uri_list(p):
    """
    prefix_uri_list : prefix_uri_list prefix_uri
    """
    p[0] = p[1] + [p[2]]

def p_single_prefix_uri_list(p):
    """
    prefix_uri_list : prefix_uri
    """
    p[0] = [p[1]]

def p_error(p):
        raise TypeError("unknown text at %r" % (p.value,))

parser = yacc.yacc(debug=0)

# Helpers

def parse(file):
    meta_data = ""
    for line in file.readlines():
        if line.startswith(PREFIX_NOTATION):
            meta_data += line[8:]
        else :
            break

    return parser.parse(meta_data, lexer=lexer)
