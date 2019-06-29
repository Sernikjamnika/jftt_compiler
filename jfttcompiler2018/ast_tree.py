import logging
import exceptions
import variables


logging.basicConfig(level=logging.ERROR)


"""
This module contains leaf structures of ast tree which 
is constructed while parsing code.
"""


class Number:
    def __init__(self, value):
        self.value = int(value)

    def generate_code(self, program, register_name='H'):
        code = []
        # optimization purposes
        if self.value < 28:
            for _ in range(self.value):
                code.append(f'INC {register_name}')
        else:
            # changing value into binary 
            while self.value != 0:
                if self.value % 2 == 0:
                    code.append(f'ADD {register_name} {register_name}')
                else:
                    code.append(f'ADD {register_name} {register_name}')
                    code.append(f'INC {register_name}')
            
                self.value //= 2
            code = code [:0:-1]
            
        code.insert(0, f'SUB {register_name} {register_name} ')
        [program.code.append(command) for command in code]
        program.line_no += len(code)
        logging.info(f"Generating number {self.value}")
        return variables.Variable('accumulator_tmp',  register_name, memory_localisation=-1)


class Value:
    def __init__(self, value):
        self.value = value

    def generate_code(self, program, register_name='H'):
        variable = self.value.generate_code(program, register_name)
        return variable

    def get_variable_names(self):
        if type(self.value) is not Number:
            return self.value.get_variable_names()
        return ()
