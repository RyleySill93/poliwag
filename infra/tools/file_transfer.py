from blessed import Terminal
from .utils import run_terminal_cmd

term = Terminal()

EXCLUDE_FILE_PATHS = [
    "*.pyc",
    ".*",
    "__pycache__",
    "__pycache__/",
]


def _build_exclude_paths() -> str:
    commands = [f'--exclude="{path}"' for path in EXCLUDE_FILE_PATHS]
    return " ".join(commands)


RSYNC_COMMAND = "rsync -rtDvz --no-t"


def run_rsync(
    ssh_key_name, ip_address: str, local_directory_path: str, target_directory_path: str
):
    print(
        term.limegreen(f"Starting rsync of {local_directory_path} to {ip_address}...")
    )
    rsync_cmd = f'{RSYNC_COMMAND} {_build_exclude_paths()} -e "ssh -i {ssh_key_name}" {local_directory_path} ubuntu@{ip_address}:{target_directory_path}'
    run_terminal_cmd(rsync_cmd)


SCP_COMMAND = "scp -r"


def run_scp(
    ssh_key_name, ip_address: str, local_directory_path: str, target_directory_path: str
):
    """
    scp -r -i bitlaunch_rsa frontend/dist root@206.166.251.49:/var/www/poliwag/frontend/dist
    """
    print(term.limegreen(f"Starting scp of {local_directory_path} to {ip_address}..."))
    scp_command = f"{SCP_COMMAND} -i {ssh_key_name} {local_directory_path} ubuntu@{ip_address}:{target_directory_path}"
    run_terminal_cmd(scp_command)


def run_reverse_scp(
    ssh_key_name, ip_address: str, local_directory_path: str, target_directory_path: str
):
    """
    scp something from server to local
    """
    print(term.limegreen(f"Starting scp of {ip_address} to {local_directory_path}..."))
    scp_command = f"{SCP_COMMAND} -i {ssh_key_name} ubuntu@{ip_address}:{target_directory_path} {local_directory_path}"
    run_terminal_cmd(scp_command)
