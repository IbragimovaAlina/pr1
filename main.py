import os
import sys
import shlex
import re
import argparse
import json

class Shell:
    def __init__(self, vfs_path="vfs.json"):
        self.physical_vfs_path = os.path.abspath(vfs_path)
        self.vfs_name = os.path.basename(self.physical_vfs_path)
        self.vfs_root = None
        self.cwd_node = None
        self.load_vfs()
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
            "vfs-init": self.cmd_vfs_init,
        }

    def load_vfs(self):
        try:
            with open(self.physical_vfs_path, 'r', encoding='utf-8') as f:
                vfs_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vfs_data = {"type": "directory", "children": {}}
        def add_parent_refs(node, parent):
            node['parent'] = parent
            if node['type'] == 'directory':
                for child in node['children'].values():
                    add_parent_refs(child, node)
        add_parent_refs(vfs_data, None)
        self.vfs_root = vfs_data
        self.cwd_node = self.vfs_root

    def get_path_str(self, node):
        if node is self.vfs_root:
            return "/"
        path_parts = []
        curr = node
        while curr is not self.vfs_root:
            for name, child in curr['parent']['children'].items():
                if child is curr:
                    path_parts.append(name)
                    break
            curr = curr['parent']
        return "/" + "/".join(reversed(path_parts))

    def resolve_path(self, path):
        if path.startswith('/'):
            current_node = self.vfs_root
            path_parts = path.strip('/').split('/')
        else:
            current_node = self.cwd_node
            path_parts = path.split('/')

        if path_parts == ['']: return current_node

        for part in path_parts:
            if not part or part == '.':
                continue
            if part == '..':
                if current_node['parent']:
                    current_node = current_node['parent']
            elif current_node['type'] == 'directory' and part in current_node['children']:
                current_node = current_node['children'][part]
            else:
                return None
        return current_node


    def cmd_vfs_init(self, args):
        print("Initializing VFS to default state.")
        default_vfs_data = {"type": "directory", "children": {}}
        default_vfs_data['parent'] = None
        self.vfs_root = default_vfs_data
        self.cwd_node = self.vfs_root
        try:
            if os.path.exists(self.physical_vfs_path):
                os.remove(self.physical_vfs_path)
                print(f"Removed physical VFS file: {self.physical_vfs_path}")
        except OSError as e:
            print(f"Error removing physical VFS file: {e}")
        print("VFS has been reset.")

    def cmd_ls(self, args):
        print("Command: ls; " + f"arguments: {args}")

    def cmd_cd(self, args):
        print("Command: cd; " + f"arguments: {args}")

    def cmd_exit(self, args):
        print("Shutting down the emulator.")
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
                    # prompt = f"{self.vfs_name}> "
                    prompt = f"[{self.vfs_name}{self.get_path_str(self.cwd_node)}]$ "

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
                # prompt = f"{self.vfs_name}> "
                prompt = f"[{self.vfs_name}{self.get_path_str(self.cwd_node)}]$ "

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
    parser.add_argument('-v', '--vfs-path', default="vfs_max.json", help="Path to the virtual file system's physical location. Default is the current directory.")
    # while (true):
    if script != "-":
        parser.add_argument('-s', '--startup-script', default=script, help="Path to a startup script with commands to execute.")
    else:
        parser.add_argument('-s', '--startup-script', help="Path to a startup script with commands to execute.")
    args = parser.parse_args()

    print(f"VFS Path: {os.path.abspath(args.vfs_path)}")
    print(f"Startup Script: {args.startup_script or 'Not provided'}")
    print("-"*50)

    shell = Shell(vfs_path=args.vfs_path)
    if args.startup_script:
        shell.run_script(args.startup_script)

    shell.run()