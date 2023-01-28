import subprocess
from typing import List
from blessed import Terminal
import paramiko

term = Terminal()


class TerminalCMDError(Exception):
    ...


def run_terminal_cmd(cmd: str):
    print(term.blue(cmd))
    rsyncproc = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    while True:
        next_line = rsyncproc.stdout.readline().decode("utf-8").rstrip()
        if not next_line:
            break
        print(term.lightgreen(next_line))

    exitcode = rsyncproc.wait()
    # check exit code
    if exitcode != 0:
        print(term.red("WARNING: An error occurred!"))
        raise TerminalCMDError("Error Occurred while executing cmd!")


def run_commands_remote(ssh_key_name, ip_address: str, commands: List[str]):
    commands = " ; ".join(commands)

    # setup from OP code
    ssh = paramiko.SSHClient()
    # ssh.load_host_keys("pth/to/known_hosts")
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    my_key = paramiko.RSAKey.from_private_key_file(ssh_key_name)
    ssh.connect(ip_address, username="ubuntu", pkey=my_key)

    # use here document to feed module into python interpreter
    stdin, stdout, stderr = ssh.exec_command(commands)
    is_error = stdout.channel.recv_exit_status() != 0
    for line in stdout:
        print(term.yellow(line), end="")

    for line in stderr:
        print(term.red(line), end="")

    if is_error:
        raise TerminalCMDError("Fuck! We got an unhealthy exit code!")
