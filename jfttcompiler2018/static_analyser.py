import exceptions
import re
import loops
import jump_fillers
import operations
import identifiers
import exceptions

from operator import itemgetter, attrgetter

class StaticAnalyser:
    def __init__(self, code, lexer, parser):
        self.code = code
        self.lexer = lexer 
        self.parser = parser
        self._nesting = 0

    def analyze_code(self):
        tokens = self.lexer.tokenize(self.code)
        program = self.parser.parse(tokens)
        # create ignored variables list
        ignored_variables = self._create_ignored_variables()

        self._nesting = 0
        try:

            while program.stack:
                command = program.stack.pop()
                self._calculate_variable_max_nesting(command)
                if command is not None:
                    command.generate_code(program)

            # self._calculate_variable_max_nesting(program)
            self.__sort_variables()

        except exceptions.UndeclaredVariable:
            pass
        # split code into lines 
        self.code_lines = self._split_code_to_lines(self.code)
        # create list of tokens
        self.tokens = self._create_token_list(self.lexer.tokenize(self.code))
        # split tokens into lines of declaration part and commands part
        self.declarations, self.commands = self._split_tokens()

        if self._check_type('WRITE') is False and self._check_type('READ') is False:
            return '' , []

        return '\n'.join(self.code_lines), ignored_variables

    def _split_code_to_lines(self, code):
        code = re.sub(r'(\s)*\[(.|\s)*?\]', '\n', code)
        code = code.split('\n')
        result = []
        for line in code:
            if line != '':
                result.append(line)
        return result

    def _split_tokens(self):
        token_number = 0
        while self.tokens[token_number].type != 'IN':
            token_number += 1
        declarations_queue = self.tokens[1:token_number]
        commands_queue = self.tokens[token_number + 1:-1]

        declarations = self.__tokens_split_to_lines(declarations_queue)
        commands = self.__tokens_split_to_lines(commands_queue)

        return declarations, commands

    def _get_line_of(self, token_type):
        appear_lines = []
        for line_number, line in enumerate(self.code_lines):
            if token_type in line:
                appear_lines.append(line_number + 1)

        return appear_lines

    def _create_token_list(self, token_generator):
        tokens = []
        for token in token_generator:
            tokens.append(token)
        return tokens

    def _create_ignored_variables(self):
        ignored_variables = []
        for variable in self.parser.variables_use.values():
            if variable.uses == 0:
                ignored_variables.append(variable.name.split('(')[0])
        return ignored_variables

    def _check_type(self, token_type):
        is_type = False
        for token in self.tokens:
            if token.type == token_type:
                is_type = True
        return is_type

    def _calculate_variable_max_nesting(self, command):
        loops_types = (
            loops.WhileLoop, 
            loops.DoWhileLoop, 
            loops.ForDownToLoop, 
            loops.ForLoop
        )

        if isinstance(command, loops_types):
            self._nesting += 1
        elif isinstance(command, jump_fillers.LoopJumpFiller):
            self._nesting -= 1

        if hasattr(command, "get_variable_names"):
            variables = command.get_variable_names()
            for variable in variables:
                variable = self.parser.variables_use.get(variable)
                if variable:
                    variable.max_nesting = max(variable.max_nesting, self._nesting)
            
    def __tokens_split_to_lines(self, commands, delimeter_type='SEMICOLON'):
        splitted_commands = []
        tmp = []

        while commands:
            token = commands.pop(0)
            tmp.append(token)
            if token.type == 'SEMICOLON':
                splitted_commands.append(tmp)
                tmp = []

        return splitted_commands

    def __increase_max_nesting(self, identifier, variables, nesting):
        if isinstance(identifier, identifiers.Identifier):
            tmp_variable = variables[identifier.value]
            tmp_variable.max_nesting = max(nesting, tmp_variable.max_nesting)
        elif isinstance(identifier, identifiers.ArrayIdentifier):
            tmp_variable = variables[identifier.identifier]
            tmp_variable.max_nesting = max(nesting, tmp_variable.max_nesting)
            self.__increase_max_nesting(identifier.index, variables, nesting)

    def __sort_variables(self):
        """
        Sorts variables by own invented heuristics.
        Sorting is stable.
        """
        sorted_variables = sorted(self.parser.variables_use.values(), key=attrgetter('max_nesting', 'uses'), reverse=True)
        sorted_variables = sorted(sorted_variables, key=attrgetter('is_array', 'start_index', 'length'))
        declarations = re.findall(r'(?<=DECLARE)((.*\n)*)(?=IN)', self.code)
        if declarations and not declarations[0][0].isspace():
            self.code = self.code.replace(declarations[0][0],' ' + '; '.join([variable.name for variable in sorted_variables]) + '; ')

