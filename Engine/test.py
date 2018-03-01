# -*- coding: utf-8 -*-
from ply import lex, yacc

from Decomposer.services import Query, Argument, Triple, UnionBlock, JoinBlock, Optional, Filter, Expression

# Lexer

reserved = {
    'UNION': 'UNION',
    'FILTER': 'FILTER',
    'OPTIONAL': 'OPTIONAL',
    'SELECT': 'SELECT',
    'DISTINCT': 'DISTINCT',
    'WHERE': 'WHERE',
    'LIMIT': 'LIMIT',
    'OFFSET': 'OFFSET',
    'ORDER': 'ORDER',
    'BY': 'BY',
    'DESC': 'DESC',
    'ASC': 'ASC',
    'BOUND': 'BOUND',
    'REGEX': 'REGEX',
    'ISIRI': 'ISIRI',
    'ISURI': 'ISURI',
    'ISBLANK': 'ISBLANK',
    'ISLITERAL': 'ISLITERAL',
    'LANG': 'LANG',
    'DATATYPE': 'DATATYPE',
    'SAMETERM': 'SAMETERM',
    'LANGMATCHES': 'LANGMATCHES',
    'STR': 'STR',
    'UCASE': 'UCASE',
    'LCASE': 'LCASE',
    'CONTAINS': 'CONTAINS',
    'UPPERCASE': 'UPPERCASE',
}

tokens = [
             #    "RDFTYPE",
             "CONSTANT",
             "NUMBER",
             "VARIABLE",
             "LKEY",
             "RKEY",
             "COLON",
             "POINT",
             "COMA",
             "URI",
             "ALL",
             "LPAR",
             "RPAR",
             "EQUALS",
             "NEQUALS",
             "LESS",
             "LESSEQ",
             "GREATER",
             "GREATEREQ",
             "ID",
             "NEG",
             "AND",
             "PLUS",
             "MINUS",
             "TIMES",
             "DIV",
             "DOUBLE",
             "INTEGER",
             "DECIMAL",
             "FLOAT",
             "STRING",
             "BOOLEAN",
             "DATETIME",
             "NONPOSINT",
             "NEGATIVEINT",
             "LONG",
             "INT",
             "SHORT",
             "BYTE",
             "NONNEGINT",
             "UNSIGNEDLONG",
             "UNSIGNEDINT",
             "UNSIGNEDSHORT",
             "UNSIGNEDBYTE",
             "POSITIVEINT",
             "OR",
            "PREFIX",
         ] + list(reserved.values())



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value.upper(), 'ID')  # Check for reserved words
    return t


t_CONSTANT = r"(\"|\')[^\"\'\n\r]*(\"|\')((@[a-z][a-z]) | (\^\^\w+))?"
t_NUMBER = r"([0-9])+"
t_VARIABLE = r"([\?]|[\$])([A-Z]|[a-z])\w*"
t_LKEY = r"\{"
t_LPAR = r"\("
t_RPAR = r"\)"
t_COLON = r"\:"
# t_RDFTYPE = r"a"
# t_RKEY = r"(\.)?\}"
t_RKEY = r"(\.)?\s*\}"
t_POINT = r"\."
t_COMA = r"\,"
t_EQUALS = r"="
t_NEQUALS = r"\!="
t_LESS = r"<"
t_LESSEQ = r"<="
t_GREATER = r">"
t_GREATEREQ = r">="
t_URI = r"<\S+>"
t_ALL = r"\*"
t_NEG = r"\!"
t_AND = r"\&\&"
t_OR = r"\|\|"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIV = r"/"
t_DOUBLE = r"xsd\:double"
t_INTEGER = r"xsd\:integer"
t_DECIMAL = r"xsd\:decimal"
t_FLOAT = r"xsd\:float"
t_STRING = r"xsd\:string"
t_BOOLEAN = r"xsd\:boolean"
t_DATETIME = r"xsd\:dateTime"
t_NONPOSINT = r"xsd\:nonPositiveInteger"
t_NEGATIVEINT = r"xsd\:negativeInteger"
t_LONG = r"xsd\:long"
t_INT = r"xsd\:int"
t_SHORT = r"xsd\:short"
t_BYTE = r"xsd\:byte"
t_NONNEGINT = r"xsd\:nonNegativeInteger"
t_UNSIGNEDLONG = r"xsd\:unsignedLong"
t_UNSIGNEDINT = r"xsd\:unsignedInt"
t_UNSIGNEDSHORT = r"xsd\:unsignedShort"
t_UNSIGNEDBYTE = r"xsd\:unsignedByte"
t_POSITIVEINT = r"xsd\:positiveInteger"
t_PREFIX = r"@prefix"
t_ignore = ' \t\n\r'


# @Shenjun
# t_ABBRE = r"(?!<)[a-z](\S)*(?=: )"

def t_error(t):
    raise TypeError("Unknown text '%s' in line %d " % (t.value, t.lexer.lineno,))


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


lexer = lex.lex(debug=1)


# Parser


if __name__ == "__main__":
    # 测试数据
    s = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    
    '''
    # Give the lexer some input
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok: break
        print '(', tok.type, ',' + str(tok.value) + ')'