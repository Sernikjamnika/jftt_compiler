import logging
import ast_tree
import variables


def less_or_equal(variable_x, variable_y, program, swap=False):
    x, y = variable_x.register, variable_y.register

    logging.info('Less or equal generating code')
    label_false = "<replace_here>"
    line_to_fill = program.line_no + 3
    if swap:
        x, y = y, x

    # NOTE x and y should become busy but here we
    # don't ask for registers so they are safe

    out_code = [
        f'COPY A {x} #condition begining ',
        f'SUB A {y}',
        f'JZERO A {program.line_no + 4}',
        f'JUMP {label_false} #condtion end'
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return [line_to_fill]

def greater_than(variable_x, variable_y, program, swap=False):
    x, y = variable_x.register, variable_y.register

    logging.info('Greater than generating code')
    label_false = "<replace_here>"
    line_to_fill = program.line_no + 4
    if swap:
        x, y = y, x

    # NOTE x and y should become busy but here we
    # don't ask for registers so they are safe

    out_code = [
        f'COPY A {y} #condition begining ',
        f'INC A',
        f'SUB A {x}',
        f'JZERO A {program.line_no + 5}',
        f'JUMP {label_false} #condtion end'
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return [line_to_fill]

def equals(variable_x, variable_y, program, negate=False):
    logging.info('Equals generating code')

    x, y = variable_x.register, variable_y.register

    label_false = "<replace_here>"
    label_true = program.line_no + 8

    if negate:
        label_false, label_true = program.line_no + 7, label_false
        lines_to_fill = [program.line_no + 6]
    else:
        lines_to_fill = [program.line_no + 3, program.line_no + 7]

    out_code = [
        f'COPY A {y} # equals',
        f'SUB A {x}',
        f'JZERO A {program.line_no + 4}',
        f'JUMP {label_false}',
        f'COPY A {x}',
        f'SUB A {y}',
        f'JZERO A {label_true} # end for not equals',
        f'JUMP {label_false} # end equals',
    ]

    # delete last jump from notequal (so hard optimazition)
    if negate:
        out_code = out_code[:-1]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    # return number of line where jump label should be replaced
    return lines_to_fill

def add(variable_x, variable_y, program):
    x = variable_x.register
    y = variable_y.register


    # optimazition purposes but didnt want to swap xD

    out_code = [
        f'ADD {x} {y}'
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'G', -1)

def sub(variable_x, variable_y, program):
    x = variable_x.register
    y = variable_y.register

    # optimazition purposes but didnt want to swap xD


    out_code = [
        f'SUB {x} {y}',
    ]
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)


    return variables.Variable('helper', 'G', -1)

def multiply(variable_x, variable_y, program):

    x = variable_x.register
    y = variable_y.register
    result_register = 'D'
    tmp_register = 'E'
    out_code = [
        f'COPY A {y} #checking which is bigger',
        f'SUB A {x}',
        f'JZERO A {program.line_no + 13}',
        f'COPY A {y} #multiplying if x is smaller',
        f'COPY {tmp_register} {x}',
        f'SUB {result_register} {result_register}',
        f'JZERO {tmp_register} {program.line_no + 23}',
        f'JODD {tmp_register} {program.line_no + 9}',
        f'JUMP {program.line_no + 10}',
        f'ADD {result_register} A',
        f'ADD A A',
        f'HALF {tmp_register}',
        f'JUMP {program.line_no + 6} # multiplying if x end',
        f'COPY A {x} #multiplying if y is smaller',
        f'COPY {tmp_register} {y}',
        f'SUB {result_register} {result_register}',
        f'JZERO {tmp_register} {program.line_no + 23}',
        f'JODD {tmp_register} {program.line_no + 19}',
        f'JUMP {program.line_no + 20}',
        f'ADD {result_register} A',
        f'ADD A A',
        f'HALF {tmp_register}',
        f'JUMP {program.line_no + 16} #multiplying if y end'
    ]


    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'D', -1)

def divide(variable_x, variable_y, program, modulo=False):

    x = variable_x.register
    y = variable_y.register
    # results
    quotient = 'C'
    remainder = 'A'


    # temporary registers
    helper_d = 'D'
    helper_e = 'E'


    if modulo:
        quotient, remainder = remainder, quotient


    out_code = [
        f'COPY {remainder} {x} #division',
        f'JZERO {y} {program.line_no + 24} #zero_divison',
        f'COPY {helper_d} {y}',
        f'COPY {quotient} {helper_d}',
        f'SUB {quotient} {remainder}',
        f'JZERO {quotient} {program.line_no + 7}',
        f'JUMP {program.line_no + 9}',
        f'ADD {helper_d} {helper_d}',
        f'JUMP {program.line_no + 3}',
        f'SUB {quotient} {quotient}',
        f'COPY {helper_e} {helper_d}',
        f'SUB {helper_e} {remainder}',
        f'JZERO {helper_e} {program.line_no + 16}',
        f'ADD {quotient} {quotient}',
        f'HALF {helper_d}',
        f'JUMP {program.line_no + 20}',
        f'ADD {quotient} {quotient}',
        f'INC {quotient}',
        f'SUB {remainder} {helper_d}',
        f'HALF {helper_d}',
        f'COPY {helper_e} {y}',
        f'SUB {helper_e} {helper_d}',
        f'JZERO {helper_e} {program.line_no + 10}',
        f'JUMP {program.line_no + 26}',
        f'SUB {remainder} {remainder}',
        f'SUB {quotient} {quotient} #division end',
    ]


    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    # return proper result based on modulo flag
    if modulo:
        return variables.Variable('helper', remainder, -1)
    else:
        return variables.Variable('helper', quotient, -1)

def decrement(variable_x, variable_y, program):
    x = variable_x.register

    out_code = [f'DEC {x}' for _ in range(variable_y)]
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'G', -1)

def increment(variable_x, variable_y, program):
    x = variable_x.register
    out_code = [f'INC {x}' for _ in range(variable_y)]
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'G', -1)

def halfing(variable_x, variable_y, program,):
    x = variable_x.register
    out_code = []
    while variable_y != 1:
        out_code.append(f'HALF {x}')
        variable_y //= 2
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'G', -1)

def bin_pow(variable_x, variable_y, program,):
    x = variable_x.register
    out_code = []
    while variable_y != 1:
        out_code.append(f'ADD {x} {x}')
        variable_y //= 2
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return variables.Variable('helper', 'G', -1)

