"""Create missing, project-local credentials for the isolated development stack."""

import argparse
import os
from pathlib import Path
from secrets import token_urlsafe
from tempfile import NamedTemporaryFile


def create_secret(path: Path) -> None:
    if path.exists():
        return
    with NamedTemporaryFile(mode="w", dir=path.parent) as secret:
        secret.write(token_urlsafe(36) + "\n")
        secret.flush()
        os.fchmod(secret.fileno(), 0o444)
        try:
            os.link(secret.name, path)
        except FileExistsError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path(".secrets"))
    args = parser.parse_args()
    directory: Path = args.directory
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if directory.stat().st_mode & 0o077:
        parser.error(f"Credential directory must be private: {directory}")
    for name in ("admin", "migration", "db", "broker", "redis"):
        create_secret(directory / f"infrapulse_{name}_password")


if __name__ == "__main__":
    main()
