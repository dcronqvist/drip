import argparse
from interpreting.interpreter import Interpreter
from parsing.parser import Parser
from lexing.lexer import Lexer
from lexing.source_pos import SourcePosition
from errors.error import Error


def prompt_drip():
    """
    Should be called when `drip` is called interactively.
    """

    out = """drip, the language."""
    print(out)


def parse_args():
    parser = argparse.ArgumentParser(description='Drip')
    parser.add_argument("file", nargs="?", help="drip script to execute.")
    return parser.parse_args()


def execute_script(source: str, file_name: str):
    lexer = Lexer(source, file_name)
    tokens, error = lexer.tokenize()

    if error:
        print(error)
        return

    parser = Parser(tokens)
    expr, error = parser.parse()
    if error:
        print(error)
        return

    interpreter = Interpreter(expr)
    result, error = interpreter.interpret()
    if error:
        print(error)
        return

    print(result)




def run_interactive():
    prompt_drip()
    while True:
        try:
            source = input("> ")
            execute_script(source, "<shell>")
        except KeyboardInterrupt as e:
            print("")
            exit(0)


if __name__ == "__main__":
    args = parse_args()

    if args.file:
        with open(args.file, "r") as f:
            source = f.read()
        execute_script(source, args.file)
    else:
        run_interactive()
