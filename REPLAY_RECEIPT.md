# Replay receipt (v0.1.0-candidate, 26 November 2026)

Release replay by the publisher from fresh copies of the approved candidate's scripts, macOS arm64. Interpreter as
printed inside the run: CPython 3.12.11, NumPy 2.3.5, SciPy 1.16.3 (see [ENVIRONMENT.txt](ENVIRONMENT.txt)).

| Program | Flags | Exit | Output vs recorded |
|---|---|---|---|
| verify.py | -I -B -O | 0 | identical; ends "All exact checks passed." |
| check_grid.py | -I -B -O | 0 | identical; ends "All 18 discrete optima match the predictions (largest gap 1.4e-14, tolerance 1e-09)." |
| Negative control | verify.py with the checked value of d_3(1) changed from −23/54 to −4/9, -I -B -O | 1 | `FAILED: d_3(1) = -23/54` |

stderr was empty for both passing runs. The lead's earlier clean replay (25 November 2026, CPython 3.11.14, NumPy
2.4.6, SciPy 1.17.1) produced byte-identical output. After the replay only the title-page DOI line of manuscript.tex,
the rebuilt PDF and the release records changed; verify.py and check_grid.py are byte-identical to the approved
candidate.

Comparison policy for other platforms (declared before tagging; also in CI, README.md and ENVIRONMENT.txt):
results/verify.txt identical; results/check_grid.txt text and integers identical, floating values within absolute
1e-9.
