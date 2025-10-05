import os
import sys
import shlex
import re
class Shell:
    def __init__(self, vfs_name="vfs"):
        self.vfs_name = vfs_name
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }
    def cmd_ls(self, args):
        print("Command: ls; " + f"arguments: {args}")
    def cmd_cd(self, args):
        print("Command: cd; " + f"arguments: {args}")
    def cmd_exit(self, args):
        print("Shutting down the emulator.")
        try:
            exit_code = int(args[0]) if args else 0
            sys.exit(exit_code)
        except ValueError:
            print("Error: exit code must be an integer.")
            sys.exit(1)
        except IndexError:
            sys.exit(0)

    def parse_line(self, line):
        expanded_line = re.sub(r'\$(\w+)', lambda m: os.getenv(m.group(1), ''), line)
        try:
            tokens = shlex.split(expanded_line, posix=False)
        except ValueError as e:
            print(f"Parsing error: {e}")
            return []
        return tokens

    def execute(self, tokens):
        if not tokens:
            return
        command_name = tokens[0]
        args = tokens[1:]
        if command_name in self.commands:
            command_func = self.commands[command_name]
            command_func(args)
        else:
            print(f"Error: command not found: {command_name}")

    def run(self):
        while True:
            prompt = f"{self.vfs_name}> "
            line = input(prompt)
            if ("$USER" in line):
                line = line.replace("$USER", "$USERNAME")
            if ("$HOME" in line):
                line = line.replace("$HOME", "$USERPROFILE")
            if ("$PWD" in line):
                line = line.replace("$PWD", "$COMPUTERNAME")
            if ("$TMPDIR" in line):
                line = line.replace("$TMPDIR", "$TEMP")
            tokens = self.parse_line(line)
            self.execute(tokens)
        print("Shell session ended.")


if __name__ == "__main__":
    shell = Shell()
    shell.run()