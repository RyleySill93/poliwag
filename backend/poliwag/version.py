import subprocess


try:
    # Assume we can get version from git until we move to containerized deploy
    VERSION = (
        subprocess.Popen(
            "git rev-parse --short HEAD",
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        .communicate()[0]
        .strip()
        .decode("utf-8")
    )
except (OSError, IOError):
    VERSION = "unknown"
