import jump_fillers
import logging


logging.basicConfig(level=logging.ERROR)


class IfThenConditional:
    def __init__(self, condition, if_commands):
        self.condition = condition
        self.if_commands = if_commands

    def generate_code(self, program):
        logging.info("IfThenConditional generating code")

        variables_copy = {}

        for variable in program.variables.values():
            variables_copy[variable.name] = variable.register

        line_to_fill = self.condition.generate_code(program)

        # if condition was not obvious there is jump to fill
        if type(line_to_fill) is not bool:
            jump_filler = jump_fillers.JumpFiller(line_to_fill, variables_copy)
            program.stack.append(jump_filler)

        # check if code of if should be generated
        if line_to_fill is not False:
            [program.stack.append(if_command) for if_command in self.if_commands]
    
    def get_variable_names(self):
        return self.condition.get_variable_names()


class IfThenElseConditional(IfThenConditional):
    def __init__(self, condition, if_commands, else_commands):
        self.else_commands = else_commands
        super().__init__(condition, if_commands)

    def generate_code(self, program):
        logging.info("IfThenElseConditional generating code")
        variables_copy = {}

        for variable in program.variables.values():
            variables_copy[variable.name] = variable.register

        line_to_fill = self.condition.generate_code(program)

        if type(line_to_fill) is not bool:
            else_jump_filler = jump_fillers.ElseJumpFiller(self.else_commands, line_to_fill, variables_copy)
            program.stack.append(else_jump_filler)
            [program.stack.append(if_command) for if_command in self.if_commands]

        # if condition is trivial
        elif line_to_fill:
            [program.stack.append(if_command) for if_command in self.if_commands]
        else:
            [program.stack.append(else_command) for else_command in self.else_commands]
