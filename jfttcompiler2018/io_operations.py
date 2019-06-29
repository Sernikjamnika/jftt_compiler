import logging
import identifiers
import ast_tree


logging.basicConfig(level=logging.DEBUG)


# DONE
class Write:
    def __init__(self, value):
        self.value = value

    def generate_code(self, program):
        logging.info('Writing')
        variable = self.value.generate_code(program, 'B')
        if variable.memory_localisation != -1:
            variable.load_from_memory(program, 'B')
        program.code.append(f'PUT B')
        program.line_no += 1
    
    def get_variable_names(self):
        if type(self.value) is not ast_tree.Number:
            return self.value.get_variable_names()
        return ()


# DONE
class Read:
    def __init__(self, identifier):
        self.identifier = identifier

    def generate_code(self, program):
        logging.info('READING')
        variable = self.identifier.get_variable(program)
        program.code.append(f'GET B')
        variable.store_in_memory(program, register='B')
        program.line_no += 1
    
    def get_variable_names(self):
        return self.identifier.get_variable_names()
