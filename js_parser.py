import ply.yacc as yacc

from js_lex import tokens
import AST

vars = {}


def p_programme_statement(p):
    ''' programme : statement
        | structure'''
    p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    ''' programme : statement programme
        | structure programme '''
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


def p_semi_colon(p):
    ''' semi_colon : ';' '''
    p[0] = AST.NoOpNode()


def p_statement(p):
    ''' statement : assignation
        | expression
        | print
        | statement semi_colon
        | semi_colon '''
    p[0] = p[1]


def p_statement_print(p):
    ''' print : CONSOLE_LOG expression '''
    p[0] = AST.PrintNode(p[2])


def p_structure(p):
    ''' structure : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2], p[4]])


def p_function_definition_arguments(p):
    ''' function_definition_arguments : IDENTIFIER
        | function_definition_arguments ',' IDENTIFIER
        | ''' # No function argument
    if len(p) == 2:
        p[0] = p[1]
        if type(p[0]) != AST.FunctionArgumentsNode:
            p[0] = AST.FunctionArgumentsNode([p[0]])
    elif len(p) == 4:
        p[0] = p[1]
        p[1].args.append(p[3])
    else:
        p[0] = AST.FunctionArgumentsNode()


def p_function_definition(p):
    ''' structure : FUNCTION IDENTIFIER  '(' function_definition_arguments ')' '{' programme '}' '''
    p[0] = AST.FunctionDefinitionNode(p[2], p[4], [p[7]])


def p_function_call_arguments(p):
    ''' function_call_arguments : expression
        | function_call_arguments ',' expression
        | ''' # No function argument
    if len(p) == 2:
        p[0] = p[1]
        if type(p[0]) != AST.FunctionArgumentsNode:
            p[0] = AST.FunctionArgumentsNode([p[0]])
    elif len(p) == 4:
        p[0] = p[1]
        p[1].args.append(p[3])
    else:
        p[0] = AST.FunctionArgumentsNode()


def p_function_call(p):
    ''' expression : IDENTIFIER '(' function_call_arguments ')' '''
    p[0] = AST.FunctionCallNode(p[1], p[3])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_unary_op(p):
    '''assignation : IDENTIFIER INC_OP'''
    p[0] = AST.UnaryNode(AST.TokenNode(p[1]), p[2])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


def p_bool(p):
    '''expression : TRUE
        | FALSE'''
    p[0] = AST.BoolNode(p[1])


def p_compare(p):
    '''expression : expression COMPARISON expression'''
    p[0] = AST.CompareNode(p[2], [p[1], p[3]])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")


precedence = (
    ('nonassoc', 'COMPARISON'), # Nonassociative operators
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated', debug=False)

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        import os

        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")
