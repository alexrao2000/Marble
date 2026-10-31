# Run this check with the bundled CPython interpreter on macOS. It executes only
# a fixed print statement and compares profiles differing by one literal read.

import json
from pathlib import Path
import subprocess
import sys
import tempfile

with tempfile.TemporaryDirectory(prefix="python-sandbox-check-") as temporary:
    directory = Path(temporary).resolve()
    program = directory / "check.py"
    program.write_text('print("ok")\n')
    reads = ["/System", "/usr", "/opt/homebrew", str(Path(sys.base_prefix).resolve()), str(directory)]
    filters = ' '.join(f'(subpath {json.dumps(p)})' for p in reads)
    filters += ' (literal "/dev/null") (literal "/dev/urandom") (literal "/dev/random")'
    for label, extra in [("without_root", ""), ("with_root", ' (literal "/")')]:
        policy = directory / "profile.sb"
        policy.write_text('(version 1)(allow default)(deny network*)(deny process-fork)'
                          f'(deny file-read-data (require-not (require-any {filters}{extra})))'
                          f'(deny file-write* (require-not (subpath {json.dumps(str(directory))})))')
        result = subprocess.run(["/usr/bin/sandbox-exec", "-f", str(policy),
                                 str(Path(sys.executable).resolve()), "-I", "-B", str(program)],
                                capture_output=True, text=True, timeout=5,
                                env={"HOME": str(directory), "PATH": "/usr/bin:/bin"})
        print(f"{label}={result.returncode} stdout={result.stdout.strip()!r}")
