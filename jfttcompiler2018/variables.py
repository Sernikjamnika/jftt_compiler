import ast_tree
import logging


logging.basicConfig(level=logging.ERROR)


class Variable:
    def __init__(self, name, register, memory_localisation, is_iterator=False):
        self.name = name
        self.register = register
        self.memory_localisation = memory_localisation
        self.is_iterator = is_iterator

    def store_in_memory(self, program, register):
        """
        Stores `variable` into memory.
        """
        ast_tree.Number(self.memory_localisation).generate_code(program, 'A')
        program.code.append(f'STORE {register} #store into memory {self.name}')
        program.line_no += 1


    def load_from_memory(self, program, register):
        """
        Loads `variable` to given register.
        """
        ast_tree.Number(self.memory_localisation).generate_code(program, 'A')
        program.code.append(f'LOAD {register} #load from memory {self.name}')
        program.line_no += 1
        self.register = register


class ArrayCell:
    def __init__(self, name, memory_localisation, parent, register = None):
        self.name = name
        self.memory_localisation = memory_localisation # index
        self.register = register
        self.parent = parent

    def store_in_memory(self, program, register):
        """
        Stores `array cell` into memory.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 'A')

            ast_tree.Number(self.parent.memory_localisation).generate_code(program)

            program.code.append('ADD A H')

            program.code.append(f'STORE {register} # end store into memory ')

            self.register = register
            program.line_no += 2
        else:
            ast_tree.Number(self.memory_localisation + self.parent.memory_localisation).generate_code(program, 'A')
            program.code.append(f'STORE {register} # store into memory {self.parent.arrName}({self.name})')
            program.line_no += 1

    def load_from_memory(self, program, register):
        """
        Loads `array cell` to given register.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 'A')

            ast_tree.Number(self.parent.memory_localisation).generate_code(program)

            program.code.append('ADD A H')
            program.code.append(f'LOAD {register} # load from memory {self.parent.arrName}({self.memory_localisation})')
            program.line_no += 2

        else:
            ast_tree.Number(self.memory_localisation + self.parent.memory_localisation).generate_code(program, 'A')
            program.code.append(f'LOAD {register} # load from memory {self.parent.arrName}({self.memory_localisation})')
            program.line_no += 1


class ArrayVariable:
    def __init__(self, arrName, start_index, end_index, memory_localisation):
        self.arrName = arrName
        self.memory_localisation = memory_localisation
        self.start_index = start_index
        self.end_index = end_index
        self.cells = dict()