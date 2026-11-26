# SPDX-License-Identifier: MIT
"""Compare fresh outputs with the recorded ones under the declared policy (also in README.md, ENVIRONMENT.txt and
REPLAY_RECEIPT.md): results/verify.txt identical byte for byte; results/check_grid.txt with identical text and integers,
floating values (numbers containing '.' or an exponent) within absolute 1e-9.
usage: compare_outputs.py FRESH_DIR RECORDED_DIR"""
import re, sys
from pathlib import Path
fresh, rec = Path(sys.argv[1]), Path(sys.argv[2])
NUM = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')
bad = []
if (fresh / 'verify.txt').read_bytes() != (rec / 'results' / 'verify.txt').read_bytes():
    bad.append('verify.txt differs')
a = (fresh / 'check_grid.txt').read_text().splitlines()
b = (rec / 'results' / 'check_grid.txt').read_text().splitlines()
if len(a) != len(b):
    bad.append('check_grid.txt line count differs')
for i, (x, y) in enumerate(zip(a, b)):
    if x == y:
        continue
    nx, ny = NUM.findall(x), NUM.findall(y)
    if NUM.split(x) != NUM.split(y) or len(nx) != len(ny):
        bad.append(f'check_grid.txt line {i + 1}: text differs'); continue
    for p, q in zip(nx, ny):
        if p == q:
            continue
        if re.fullmatch(r'[-+]?\d+', p) or re.fullmatch(r'[-+]?\d+', q) or abs(float(p) - float(q)) > 1e-9:
            bad.append(f'check_grid.txt line {i + 1}: {p} vs {q}')
if bad:
    print('DIFFERENCES:', *bad, sep='\n  '); sys.exit(1)
print('OK verify.txt identical; check_grid.txt within the declared policy')
