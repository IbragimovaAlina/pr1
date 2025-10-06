import os
import sys
import shlex
import re
import argparse
class Shell:
    def __init__(self, vfs_path="."):
        self.vfs_path = vfs_path
        self.vfs_name = os.path.basename(os.path.abspath(vfs_path))
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

    def run_script(self, script_path):
        print(f"Running from script: {script_path}")
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    prompt = f"{self.vfs_name}> "
                    print(f"{prompt}{line}")
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
        except FileNotFoundError:
            print(f"Error: Startup script not found at '{script_path}'")
        except Exception as e:
            print(f"An unexpected error: {e}")
        print("Startup script finished")


    def run(self):
        print("\nWelcome to the simple shell emulator! Type 'exit' to quit.")
        while True:
            try:
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
            except (KeyboardInterrupt, EOFError):
                print("\nExiting shell...")
                break
        print("Shell session ended.")


if __name__ == "__main__":
    print("Enter the name of the file with the startup script (if you don't need it, enter '-')")
    script = input()
    parser = argparse.ArgumentParser(description="A simple shell emulator.")
    parser.add_argument(
        '-v', '--vfs-path',
        default=".",
        help="Path to the virtual file system's physical location. Default is the current directory."
    )
    if script != "-":
        parser.add_argument(
            '-s', '--startup-script', default=script,
            help="Path to a startup script with commands to execute."
        )
    else:
        parser.add_argument(
            '-s', '--startup-script',
            help="Path to a startup script with commands to execute."
        )
    args = parser.parse_args()
    print(f"VFS Path: {os.path.abspath(args.vfs_path)}")
    print(f"Startup Script: {args.startup_script or 'Not provided'}")
    print("-"*50)
    shell = Shell(vfs_path=args.vfs_path)
    if args.startup_script:
        shell.run_script(args.startup_script)

    shell.run()