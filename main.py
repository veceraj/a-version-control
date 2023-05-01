import argparse
import config
import sys
import importlib


class VersionControl:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="A version control system")
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.commands = {}

        for module_name, attr in config.commands.items():
            module = importlib.import_module(module_name)
            command = getattr(module, attr)
            self.commands[module_name] = command(self.subparsers)

    def run(self):
        if len(sys.argv) == 1:
            return self.parser.print_help()

        args = self.parser.parse_args()

        if args.command not in self.commands:
            return print("Operation not supported")

        if not config.path_meta.is_file() and not args.command == "init":
            print("Version Control not initialized.")
            return

        command = self.commands[args.command]
        command.run(args)


if __name__ == "__main__":
    version_control = VersionControl()
    version_control.run()
