import AST
from AST import addToClass
from functools import reduce

operations = {
    '++': lambda x: x + 1,
    '--': lambda x: x - 1,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

comparisons = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
}

vars = {}
function_definitions = {}
functions_args = {}


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        # @todo Check if we're within a function
        if isinstance(c, AST.FunctionReturnNode):
            return c.execute()
        else:
            c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print('*** Error: variable %s undefined!' % self.tok)

    return self.tok


@addToClass(AST.StringLiteralNode)
def execute(self):
    string = self.children[1:-1] # Remove quotes around the string literal
    return string.encode('utf-8').decode('unicode_escape') # back-slash unescaping, taken from https://stackoverflow.com/questions/1885181/how-do-i-un-escape-a-backslash-escaped-string-in-python


@addToClass(AST.OpNode)
def execute(self):
    # @todo If a StringLiteralNode is given, check that only '+' operator is used
    args = [c.execute() for c in self.children]

    if len(args) == 1:
        args.insert(0, 0)

    return reduce(operations[self.op], args)


@addToClass(AST.UnaryNode)
def execute(self):
    vars[self.variable.tok] = operations[self.children](vars[self.variable.tok])


@addToClass(AST.DeclareNode)
def execute(self):
    """
    Almost the same than AssignNode execute method
    except that a variable can be declared without any assignation
    """
    identifier = self.children[0].tok

    if len(self.children) > 1:
        vars[identifier] = self.children[1].execute()
    else:
        vars[identifier] = None


@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()


@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())


@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.BoolNode)
def execute(self):
    if isinstance(self.bool, str):
        if self.bool == 'true':
            self.bool = True
        elif self.bool == 'false':
            self.bool = False

    return self.bool


@addToClass(AST.CompareNode)
def execute(self):
    comparison = comparisons[self.comparison](self.children[0].execute(), self.children[1].execute())
    return AST.BoolNode(comparison).execute()


@addToClass(AST.FunctionArgumentsNode)
def execute(self):
    for arg in self.args:
        # Compute the values the function was called with (could be an expression)
        AST.TokenNode(arg).execute()


@addToClass(AST.FunctionDefinitionNode)
def execute(self):
    if isinstance(self.identifier, str):
        # Registers the function definition and its arguments
        function_definitions[self.identifier] = self.children[0]
        functions_args[self.identifier] = self.args


@addToClass(AST.FunctionReturnNode)
def execute(self):
    if self.children:
        return self.children[0].execute()

    return None


@addToClass(AST.FunctionCallNode)
def execute(self):
    if isinstance(self.children, str):
        try:
            tmp_variables = copy_tmp_variables(self.children, self.args)
            result = function_definitions[self.children].execute()
            clear_tmp_variables(self.children, tmp_variables)

            return result
        except KeyError:
            print('*** Error: function %s undefined!' % self.children)


@addToClass(AST.NoOpNode)
def execute(self):
    pass


def copy_tmp_variables(function_identifier, args):
    """
    This function and clear_tmp_variables function are designed to "simulate" JS global and local variables scopes.

    :param function_identifier:
    :param args:
    :return:
    """
    # Dict of dict to hold values of global and local scope
    tmp_variables = {
        'global': dict(),
        'local': dict(),
    }

    # Make sure that there is no declaration in the function that could overwrite global variables
    # and mark the local variables in order to delete them when the function returns
    for instructions in function_definitions[function_identifier].children:
        if isinstance(instructions, AST.DeclareNode):
            variable_name = instructions.children[0].tok

            if variable_name in vars:
                # The global variable will be shadowed by the local variable
                # let's save its current value to restore it when the function returns
                tmp_variables['global'][variable_name] = vars[variable_name]
            else:
                # if the variable doesn't currently exist, then it is a local variable
                # let's mark it to delete it when the function returns
                tmp_variables['local'][variable_name] = True

    # Make sure that there no argument which were given to the function could overwrite global variables
    if functions_args[function_identifier].args:
        for arg in functions_args[function_identifier].args:
            try:
                # The global variable will be shadowed by the argument
                # let's save its current value to restore it when the function returns
                tmp_variables['global'][arg] = vars[arg]
            except KeyError:
                pass

        # Copy the given argument so the function can access it
        for identifier, value in zip(functions_args[function_identifier].args, args.args):
            vars[identifier] = value.execute()

    return tmp_variables


def clear_tmp_variables(function_identifier, tmp_variables):
    """
    This function and copy_tmp_variables function are designed to "simulate" JS global and local variables scopes.

    :param function_identifier:
    :param args:
    :return:
    """
    # Deletes the arguments which were given to the function
    if functions_args[function_identifier].args:
        for identifier in functions_args[function_identifier].args:
            del vars[identifier]

    # Deletes the local variables
    for identifier in tmp_variables['local']:
        del vars[identifier]

    # Restores the global variables
    for identifier, value in tmp_variables['global'].items():
        vars[identifier] = value


if __name__ == '__main__':
    from js_parser import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
