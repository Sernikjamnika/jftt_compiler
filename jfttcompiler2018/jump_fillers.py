import logging


logging.basicConfig(level=logging.ERROR)


class JumpFiller:
    """
    Class for ending commands involving jumps.
    """
    def __init__(self, returning_points, variables_in_past=dict()):
        self.returning_points = returning_points
        self.variables_in_past = variables_in_past

    def generate_code(self, program):
        self.restore_variables(program)

        logging.info(f"Changing label in JUMP Command nr line {self.returning_points} value {program.line_no}")
        for returning_point in self.returning_points:
            program.code[returning_point] = program.code[returning_point].replace("<replace_here>", str(program.line_no))


    def restore_variables(self, program):
        pass


class ElseJumpFiller(JumpFiller):
    """
    Specific end for Else in If Then Else.
    """
    def __init__(self, else_commands, line_to_fill, variables_in_past=dict()):
        self.else_commands = else_commands
        self.variables_in_past = variables_in_past
        self.line_to_fill = line_to_fill

    def generate_code(self, program):
        # adds jump at the end of if in "if then else" statement
        program.code.append(f'JUMP <replace_here>')
        jump_filler = JumpFiller([program.line_no], self.variables_in_past)
        program.line_no += 1
        program.stack.append(jump_filler)
        [program.stack.append(else_command) for else_command in self.else_commands]
        condition_end = JumpFiller(self.line_to_fill)
        program.stack.append(condition_end)


# DONE
class LoopJumpFiller:
    """
    Class to end loops with proper jumps.
    """
    def __init__(self, returning_points, additional_code=(), iterator=None, variables_in_past=dict()):
        self.returning_points = returning_points
        self.iterator = iterator
        self.additional_code = additional_code
        self.variables_in_past = variables_in_past

    def generate_code(self, program):
        logging.info(f"Changing label in JUMP for loop Command nr line {program.line_no + 1} value {self.returning_points}")
        self.restore_variables(program)
        self.generate_additional_code(program)
        self.destroy_iterator(program)
        program.code.append(f'JUMP {self.returning_points} #jump to condition')
        program.line_no += 1

    def generate_additional_code(self, program):
        if type(self.additional_code) is list:
            for additional_command in self.additional_code:
                program.code.append(additional_command)
            program.line_no += len(self.additional_code)

    def destroy_iterator(self, program):
        if self.iterator is not None:
            program.variables.pop(self.iterator+'_end0')

    def restore_variables(self, program):
        pass

class ForLoopJumpFiller(LoopJumpFiller):
    """
    Specific end for For Loop with iterator incrementation and, after loop, destroying it.
    """

    def generate_code(self, program):
        iterator_variable = program.get_variable(self.iterator)
        iterator_variable.register = 'B'
        iterator_variable.load_from_memory(program, iterator_variable.register)

        program.code.append(f'INC {iterator_variable.register} # increment iterator')
        program.line_no += 1
        iterator_variable.store_in_memory(program, iterator_variable.register)

        program.code.append(f'JUMP {self.returning_points} #jump to condition')
        program.line_no += 1
        self.destroy_iterator(program)


class ForDownToLoopJumpFiller(LoopJumpFiller):
    """
    Specific end for For Down To Loop with iterator decrementation and, after loop, destroying it.
    Also secures the example when For Down To Loop reaches 0.
    """

    def generate_code(self, program):
        iterator_variable = program.get_variable(self.iterator)
        iterator_variable.register = 'B'

        iterator_variable.load_from_memory(program, iterator_variable.register)

        program.code.append(f'JZERO {iterator_variable.register} <replace_here>')
        line_to_fill = program.line_no
        program.code.append(f'DEC {iterator_variable.register} # decrement iterator')
        program.line_no += 2
        iterator_variable.store_in_memory(program, iterator_variable.register)
        program.code.append(f'JUMP {self.returning_points} #jump to condition')
        program.line_no += 1
        program.code[line_to_fill] = program.code[line_to_fill].replace("<replace_here>", str(program.line_no))

        self.destroy_iterator(program)
