import exceptions

from sly import Lexer


class JFTTLexer(Lexer):
    tokens = {
        PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, LPARENTHESIS, RPARENTHESIS, #arithmetic signs
        EQUAL, NOT_EQUAL, LESS_OR_EQUAL, GREATER_OR_EQUAL, LESS_THAN, GREATER_THAN, #relations
        IF, THEN, ELSE, ENDIF, #conditions
        WHILE, DO, ENDWHILE, ENDDO, FOR, FROM, TO, DOWNTO, ENDFOR, #loops
        READ, WRITE, #io
        NUMBER, ASSIGN, #declarations and constants
        SEMICOLON, COLON, #separators
        DECLARE, IN, END, PIDENTIFIER #program section 
    }

    ignore = ' \t'
    ignore_comment = r'\[(.|\s)*?\]'

    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    MODULO = r'\%'
    LPARENTHESIS = r'\('
    RPARENTHESIS = r'\)'

    EQUAL = r'\='
    NOT_EQUAL = r'\!\='
    LESS_OR_EQUAL = r'\<\='
    GREATER_OR_EQUAL = r'\>\='
    LESS_THAN = r'\<'
    GREATER_THAN = r'\>'

    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    DOWNTO = r'DOWNTO'


    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    ENDDO = r'ENDDO'

    FOR = r'FOR'
    FROM = r'FROM'
    TO = r'TO'
    ENDFOR = r'ENDFOR'

    READ = r'READ'
    WRITE = r'WRITE'

    ASSIGN = r'\:='

    SEMICOLON = r'\;'
    COLON = r'\:'

    DECLARE = r'DECLARE'
    IN = r'IN'
    END = r'END'

    PIDENTIFIER = r'[_a-z]+'


    @_(r'[0-9]+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling rule
    def error(self, t):
        raise exceptions.SyntaxError(self.lineno)

    