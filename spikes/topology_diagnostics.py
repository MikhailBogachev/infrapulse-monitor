"""Redact the disposable Compose fixture's credentials from captured logs."""

import re
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path
from urllib.parse import quote


def redact(lines: Iterable[str], secrets_dir: Path, private_key: Path) -> Iterator[str]:
    values: set[str] = set()
    for file in secrets_dir.glob("infrapulse_*_password"):
        value = file.read_text().strip()
        if value:
            values.update((value, quote(value, safe="")))
    if private_key.is_file():
        values.update(filter(None, private_key.read_text().splitlines()))
    sensitive = sorted(values, key=len, reverse=True)
    for line in lines:
        for value in sensitive:
            line = line.replace(value, "[redacted]")
        yield re.sub(r"(\b[a-zA-Z][\w+.-]*://)[^\s/@]+@", r"\1[redacted]@", line)


if __name__ == "__main__":
    sys.stdout.writelines(redact(sys.stdin, Path(sys.argv[1]), Path(sys.argv[2])))
