import exceptions
import logging

import ast_tree
import identifiers
import snippets

logging.basicConfig(level=logging.ERROR)


class AssignmentOperations:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def generate_code(self, program):
        logging.info("AssignmentOperations generating code")
        variable = self.identifier.get_variable(program)

        if isinstance(self.expression, ArithemticOperations):
            result_variable = self.expression.generate_code(program)
            variable.register = result_variable.register 
            variable.store_in_memory(program, result_variable.register)
        elif isinstance(self.expression.value, ast_tree.Number):
            result_variable = self.expression.generate_code(program, 'G')
            variable.register = result_variable.register
            variable.store_in_memory(program, result_variable.register)
        else:
            result_variable = self.expression.generate_code(program, 'G')
            result_variable.load_from_memory(program, 'G')
            variable.store_in_memory(program, result_variable.register)
    
    def get_variable_names(self):
        """
        Gets names of variables used in command
        """
        result = []
        result.extend(self.identifier.get_variable_names())
        result.extend(self.expression.get_variable_names())
        return tuple(result)


# DONE
class ConditionOperations:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.relations = {
            '>': lambda x, y, p: snippets.greater_than(x, y, p),
            '<=': lambda x, y, p: snippets.less_or_equal(x, y, p),
            '<': lambda x, y, p: snippets.greater_than(x, y, p, swap=True),
            '>=': lambda x, y, p: snippets.less_or_equal(x, y, p, swap=True),
            '=': lambda x, y, p: snippets.equals(x, y, p),
            '!=': lambda x, y, p: snippets.equals(x, y, p, negate=True)
        }

        self.lambdas = {
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '=': lambda x, y: x == y,
            '!=': lambda x, y: x != y
        }

    def generate_code(self, program):
        """
        Generates line to fill for condition
        """
        logging.info("ConditionOperations generating code")
        if type(self.left) is type(self.right) and type(self.left) is ast_tree.Number:
            return self.lambdas[self.op](self.left.value, self.right.value)

        left_value = self.left.generate_code(program, register_name='C')
        right_value = self.right.generate_code(program, register_name='D')

        if left_value.memory_localisation != -1:
            left_value.load_from_memory(program, left_value.register)
        if right_value.memory_localisation != -1:
            right_value.load_from_memory(program, right_value.register)


        logging.info(f'{left_value.register}, {right_value.register}')
        line_to_fill = self.relations[self.op](left_value, right_value, program)

        return line_to_fill

    def get_variable_names(self):
        """
        Gets names of variables used in command
        """
        result = []
        if type(self.left) is not ast_tree.Number:
            result.extend(self.left.get_variable_names())
        if type(self.right) is not ast_tree.Number:
            result.extend(self.right.get_variable_names())
        return tuple(result)


# DONE
class ArithemticOperations(ConditionOperations):

    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op
        self.snippets = {
            '+': lambda x, y, p: snippets.add(x, y, p),
            '-': lambda x, y, p: snippets.sub(x, y, p),
            '*': lambda x, y, p: snippets.multiply(x, y, p),
            '/': lambda x, y, p: snippets.divide(x, y, p),
            '%': lambda x, y, p: snippets.divide(x, y, p, modulo=True),
            '++': lambda x, y, p: snippets.increment(x, y, p),
            '--': lambda x, y ,p: snippets.decrement(x, y, p),
            'half':lambda x, y, p: snippets.halfing(x, y, p),
            'bin_pow': lambda x, y, p: snippets.bin_pow(x, y, p)
        }

        self.lambdas = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: max(0, x - y),
            '*': lambda x, y: x * y,
            '/': lambda x, y: x // y,
            '%': lambda x, y: x % y,
        }

    def generate_code(self, program):
        logging.info("Arithmetic snippets generating code")
        if type(self.left) is type(self.right) and type(self.left) is ast_tree.Number:
            result = ast_tree.Number(self.lambdas[self.op](self.left.value, self.right.value))
            result_variable = result.generate_code(program, 'G')
        else:
            # swap left and right if operation allows it and left is a number
            # thanks to this if we can optimize code Number is on the right side
            operation = self.op


            if self.op == '-' and self._check_enough_small(self.right):
                operation = '--'
                variable_right = self.right.value
            elif self.op == '+' and self._check_enough_small(self.right):
                operation = '++'
                variable_right = self.right.value
            elif self.op == '/' and self._check_divisible_by_two(self.right):
                operation = 'half'
                variable_right = self.right.value
            elif self.op == '*' and self._check_divisible_by_two(self.right):
                operation = 'bin_pow'
                variable_right = self.right.value
            else:
                variable_right = self.right.generate_code(program, register_name='F')


            variable_left = self.left.generate_code(program, register_name='G')

            # if same variables are only one has to be added
            if hasattr(variable_right, 'register') and variable_left.register != variable_right.register:
                if variable_right.memory_localisation != -1:
                    variable_right.load_from_memory(program, variable_right.register)
            if variable_left.memory_localisation != -1:
                variable_left.load_from_memory(program, variable_left.register)


            result_variable = self.snippets[operation](variable_left, variable_right, program)

        return result_variable

    def _check_divisible_by_two(self, right):
        """
        Checks if is divisible by two so we can make halfs or powers of two.
        """
        if type(right) is ast_tree.Number:
            right = right.value
            while right != 1:
                if right % 2 == 1:
                    return False
                right //= 2
            return True
        return False

    def _check_enough_small(self, right):
        """
        Checks if value is small enough to make incrementations (or decrementations)
        instead of adding (or substraction)
        """
        if type(right) is ast_tree.Number:
            if right.value < 28:
                return True
        return False
