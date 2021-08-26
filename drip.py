import argparse
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
    print(f"Running the script {file_name}, with source {source}.")


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

    source = "var x = 128.2 . 2"
    err = Error("SyntaxError", 2, SourcePosition(source, "<shell>").set_position(1, 14, 14), SourcePosition(source, "<shell>").set_position(1, 14, 14), "Invalid operator '.'")

    print(err)

    # if args.file:
    #     with open(args.file, "r") as f:
    #         source = f.read()
    #     execute_script(source, args.file)
    # else:
    #     run_interactive()
