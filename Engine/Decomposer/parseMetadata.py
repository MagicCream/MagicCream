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

t_PREFIX = r"[a-z](\S)*"+":"+r"[a-z](\S)*"
t_URI = r"<"+"\S+"+r">"
t_POINT= r"\."

t_ignore = ' \t\n'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()

# Parser

def p_parse_sparql(p):
    """
    parse_sparql : endpoints_list
    """
    p[0] = p[1]

def p_endpoints_list(p):
    """
    endpoints_list : endpoints_list endpoint
    """
    p[0] = p[1] + [p[2]]

def p_single_endpoint_list(p):
    """
    endpoints_list : endpoint
    """
    p[0] = [p[1]]

def p_endpoint(p):
    """
    endpoint : URI predicate_list POINT
    """
    p[0] = (p[1], p[2])

def p_predicate_list(p):
    """
    predicate_list : predicate_list predicate
    """
    p[0] = p[1] + [p[2]]

def p_single_predicate_list(p):
    """
    predicate_list : predicate
    """
    p[0] = [p[1]]

def p_predicate_0(p):
    """
    predicate : PRED0
    """
    p[0] = p[1]

def p_predicate_1(p):
    """
    predicate : PRED1
    """
    p[0] = p[1]

def p_predicate_u(p):
    """
    predicate : URI
    """
    p[0] = p[1]

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
