class UndeclaredVariable(Exception):
    def __init__(self, variable_name, line):
        message = f'Variable "{variable_name}" in line {line} of commands is not declared'
        super().__init__(message)

class StatusDoesNotExist(Exception):
    def __init__(self, status_name):
        message = f'Status "{status_name}" of register does not exist'
        super().__init__(message)
        
class DoubledDeclarationVariable(Exception):
    def __init__(self, variable_name, line_no):
        message = f'Variable "{variable_name}" has been declared more than one time in line {line_no}'
        super().__init__(message)

class ArrayWrongDeclaration(Exception):
    def __init__(self, variable_name, line_no):
        message = f'Array "{variable_name}" has been declared with start value higher than end value in line {line_no}'
        super().__init__(message)        

class IteratorManipulation(Exception):
    def __init__(self, variable_name, line_no):
        message = f'Iterator "{variable_name}" has been manipulated in line {line_no}'
        super().__init__(message)  

class VariableNotInitialized(Exception):
    def __init__(self, variable_name, line_no):
        message = f'Variable "{variable_name}" has not been initialized in line {line_no}'
        super().__init__(message)

class SyntaxError(Exception):
    def __init__(self, line_no):
        message = f'Invalid syntax in line {line_no}'
        super().__init__(message)  

class ArrrayOutOfBound(Exception):
    def __init__(self, line_no):
        message = f'Using array out of bound in line {line_no}'
        super().__init__(message)  
