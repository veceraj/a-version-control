"""Main module"""

import argparse
import sys
import importlib
import config


commands = {
    "init": "InitCommand",
    "add": "AddCommand",
    "checkout": "CheckoutCommand",
    "commit": "CommitCommand",
    "diff": "DiffCommand",
    "version": "VersionCommand",
    "reset": "ResetCommand",
    "stash": "StashCommand",
    # "mv": "MvCommand",
}


class VersionControl:
    """Version Controll"""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="A version control system")
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.commands = {}

        for module_name, attr in commands.items():
            module = importlib.import_module(module_name)
            command_module = getattr(module, attr)
            self.commands[module_name] = command_module(self.subparsers)

    def run(self):
        """Main run method entry point"""
        if len(sys.argv) == 1:
            self.parser.print_help()
            return

        args = self.parser.parse_args()

        if not config.path_meta.is_file() and not args.command == "init":
            print("Version Control not initialized.")
            return

        command_module = self.commands[args.command]
        command_module.run(args)


if __name__ == "__main__":
    version_control = VersionControl()
    version_control.run()
