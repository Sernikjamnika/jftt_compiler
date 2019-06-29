import logging
import ast_tree
import exceptions
import variables


class JFTTProgram:
    """
    Class responsible for generating assembly code from given parsed comamnds
    """

    def __init__(self, declarations, commands, variables, arrays, used_memory):
        self.declarations = declarations
        self.stack = commands
        self.code = []
        self.variables = variables
        self.arrays = arrays
        self.used_memory = used_memory
        self.line_no = 0
        #TODO delete because only for debugging purposes
        self.cells = []

        # a for accumulator
        # h for constants
        self.registers = {
            'G': None,
            'F': None,
            'E': None,
            'D': None,
            'C': None,
            'B': None,
        }

    # generate code by using commands on the stack (pseudo DFS over ast_tree)
    # when stack is empty code hit its end
    # NOTE each command must implement generate_code method

    def generate_code(self):
        """
        Generates code for whole program basing on stack of commands (DFS-like style).
        Note: some optimization can be done so result code does not have to be exactly the same as in language.
        Note: all commands must implement `generate_code` method.
        """
        self.lines = []
        while self.stack:
            command = self.stack.pop()
            if command is not None:
                command.generate_code(self)
                self.lines.append(command)

        result = ''
        for code_snippet in self.code:
            if isinstance(code_snippet, list):
                result += '\n'.join(code_snippet)
                result += '\n'
            else:
                result += code_snippet + '\n'
                
        result += 'HALT'

        return result

    def get_variable(self, variable_name):
        """
        Gets variable. If was not declared exception UndeclaredVariable
        is thrown. If variable is InMemory or used for the first time
        apropriate methods are called.
        """
        variable = self.variables.get(variable_name)
        # if is not declared
        if variable is None:
            raise exceptions.UndeclaredVariable(variable_name, self.line_no)
        return variable

    def get_register(self, register_name):
        """
        Gets exact register byb register_name.
        """
        logging.info(f"Getting register {register_name}")
        for variable_object in self.variables.values():
            if variable_object.register == register_name:
                variable_object.store_in_memory(self)
                return register_name

    def get_array_cell(self, identifier, index):
        """
        Checks if array was declared and returns array_cell.
        """
        arr = self.arrays.get(identifier)

        if arr is None:
            raise exceptions.UndeclaredVariable

        array_cell = variables.ArrayCell(identifier, index, arr)
        return array_cell


