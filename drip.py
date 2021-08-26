import argparse


def prompt_drip():
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
    if args.file:
        with open(args.file, "r") as f:
            source = f.read()
        execute_script(source, args.file)
    else:
        run_interactive()
