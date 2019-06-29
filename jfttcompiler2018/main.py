from program import JFTTProgram
from lexer import JFTTLexer
from parser import JFTTParser
from static_analyser import StaticAnalyser
import logging
import os
import sys
import re 


"""
This is compiler of simple imperative programming language - Gębalang.
It was created as part of JFTT course (Formal Languages and Translation Techniques)
during Bachelor studies at WPPT faculty (Fundamental Problems of Technology).

It takes file with program in Gębalang and creates output in simple assembly.
Than it can be processed by register machine added to this project in "../maszyna_rejestrowa"
directory.

Compiler enables to run it in testing mode with -test flag. Then it compiles all 
files in given directory.
"""


def main(input_file, output_file):
    lexer = JFTTLexer()
    parser_analysis = JFTTParser()
    parser = JFTTParser(analysis=False)

    with open(input_file, 'r') as file:
        code = file.read()
    analyzer = StaticAnalyser(code, lexer, parser_analysis)
    analyzed_code, ignored_variables = analyzer.analyze_code()
    if analyzed_code == '':
        result = 'HALT'
    else:
        parser.ignored_variables = ignored_variables
        parser.iterators = parser_analysis.iterators
        parser.variables_use = parser_analysis.variables_use
        tokens = lexer.tokenize(analyzed_code)
        program = parser.parse(tokens)
        result = program.generate_code()

    with open(output_file, 'w') as file:
        file.write(result)


if __name__ == "__main__":
    compiler_dir = os.getcwd()
    test_dir = sys.argv[1]
    outputs_dir = sys.argv[2]
    if '-test' in sys.argv:
        tests = os.listdir(test_dir)
        tests.sort()
        for test in tests:
            main(f"{test_dir}/{test}", f"{outputs_dir}/{test}")
    else:
        main(test_dir, outputs_dir)
        main(test_dir, outputs_dir)
