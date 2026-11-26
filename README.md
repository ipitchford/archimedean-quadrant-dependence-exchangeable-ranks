# Quadrant dependence, reflected copula measures and exchangeable ranks

**All four Fuchs–Tschimpke implications fail, and exact limits for exchangeable ranks**

Version 0.1.0-candidate. DOI [10.5281/zenodo.24547093](https://doi.org/10.5281/zenodo.24547093) (all versions:
[10.5281/zenodo.24547092](https://doi.org/10.5281/zenodo.24547092)). Release page:
https://evidencepress.org/releases/archimedean-quadrant-dependence-exchangeable-ranks/

**Status: unrefereed research candidate.** Assurance is internal AI-assisted review, a proof audit and exact
computational checks only (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)). It is not peer review, independent
reproduction or formal verification. Creator: Anonymous.

## What this is about

Statisticians describe how two quantities move together (losses on two loans, rainfall at two sites) with a
*copula*: the joint behaviour of their ranks, free of the units each quantity is measured in. Two ideas of "positive
dependence" are in play.

- **Quadrant dependence (PQD)** says that jointly low values are at least as likely as they would be under
  independence, at every pair of thresholds.
- The newer **positive measure inducing (PMI)** property of Fuchs and Tschimpke compares, rectangle by rectangle, the
  probability on the main-diagonal side of the square with the probability on the opposite side.

PMI forces an ordering of popular rank correlations, for example 3 times Gini's gamma is at least 2 times Spearman's
rho, and Fuchs and Tschimpke built tests on this. They conjectured that for Archimedean copulas, the workhorse family
in finance, insurance and hydrology, PMI is the same as quadrant dependence (and likewise for the negative versions).
If so, failing their test would rule out every positively dependent Archimedean model. Graham (2026) gave one
counterexample (quadrant dependent but not PMI) and left the other three directions open.

## What is new

1. **All four directions fail**, with simple smooth Archimedean examples as close to independence as you like and
   explicit parameters (one in a thousand and one in a hundred million). One of them is quadrant dependent yet
   reverses the rank inequality, so a violation of 3γ ≥ 2ρ does not rule out every quadrant dependent Archimedean
   model.
2. **No finite test battery suffices.** Comparing rank correlations detects exactly the symmetrised reflected measure;
   for exchangeable copulas it characterises PMI, but only with infinitely many comparisons.
3. **Shared frailty.** Two frailty levels always give PMI; three (rates 1, 2 and 200) can break it, even with a
   density that is totally positive of every order.
4. **Clusters of interchangeable units.** If the two ranks come from a group of n exchangeable units, the
   combination 3γ − 2sρ has an exact lower limit for every slope −n/2 ≤ s ≤ 1: −(3 − 2s)/(n − 1) for even n, with
   an explicit parity correction for odd n. For three units, Gini's gamma is never below −4/9 and 3γ − 2ρ never below
   −23/54, compared with −1 with no constraint.
5. **Generalised Gini matrices.** The same construction settles the smallest common pairwise generalised Gini
   correlation in any number of variables, a question left open by Koike and Hofert (whose Gaussian example reaches
   about −0.379 for n = 3, against the correlation-matrix bound −1/2).

**Idea of the proofs.** Nudge the independence copula by a small polynomial and track two signs, one for the
cumulative comparison and one for the local reflected comparison; they can be chosen independently. For clusters,
write each rank as a sign and a size; with an odd number of units the signs cannot all cancel, and that leftover sign
costs a fixed amount of correlation.

## Limits

- The counterexamples are tiny effects (3γ − 2ρ of order 10⁻¹⁰ and 10⁻⁵ at the explicit parameters) and say nothing
  about the power of tests in real samples.
- All results are population statements; no finite-sample test of the cluster limits is given.
- The full set of attainable rank correlations for exchangeable ranks, and the full set of generalised Gini
  correlation matrices, remain open (Section 8 of the paper).

## Credits

Fuchs and Tschimpke (PMI definition, ordering theorem, conjecture); Graham (first counterexample); Ansari, Rockel and
Steinmaßl (sign–magnitude representation of ρ and γ); Koike and Hofert (generalised Gini representation and
compatibility bounds); Fuchs (2024) (conditionally i.i.d. representation); Müller and Scarsini (MTP2 criterion);
McNeil and Nešlehová; Konstantopoulos and Yuan. Bibliography: [refs.bib](refs.bib).

## Contents

| File | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (14 pages; standard LaTeX packages, no figures) |
| [verify.py](verify.py) | Standard library only, exact rational arithmetic: every exact constant of the paper (effect-size slopes, density bounds, the three-rate frailty certificate, closed forms and attainment of d_n(s), −23/54, −4/9, Remark 6.4, J_k = 1/k) |
| [check_grid.py](check_grid.py) | NumPy/SciPy: finite-grid linear programs for the exchangeability theorem (18 cases); tests the extremal mechanism on atomic grids, does not prove the theorem |
| [results/verify.txt](results/verify.txt), [results/check_grid.txt](results/check_grid.txt) | Recorded outputs |
| [AI_INDEX.md](AI_INDEX.md) | Machine-oriented map of claims, evidence and limits |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [RESEARCH_GATES.json](RESEARCH_GATES.json) | Review summary; prior-art and limitation records |
| [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Replay record and environment |
| [CITATION.cff](CITATION.cff), [LICENSE.md](LICENSE.md), [MANIFEST.sha256](MANIFEST.sha256) | Citation, licences, hashes |

## Replay

From the package root:

```sh
python3 -I -B -O verify.py                 # standard library; < 1 s; ends "All exact checks passed."
pip install -r requirements.txt            # numpy, scipy (check_grid.py only)
python3 -I -B -O check_grid.py             # ~10 s; ends "All 18 discrete optima match the predictions ..."
```

Both scripts stop with a `FAILED` message and a nonzero exit on any failed check (no `assert`, so the checks stay
active under `python -O`). Comparison policy (declared before tagging; the same in CI, ENVIRONMENT.txt and
REPLAY_RECEIPT.md): `results/verify.txt` must be identical byte for byte; in `results/check_grid.txt` every text and
integer must be identical and the printed floating values (LP optima, predictions and the largest gap) may differ in
the last places across platforms, within absolute 1e-9, the script's own declared tolerance.

## Licences

Text, the paper, recorded outputs and records: CC0-1.0. Code (`*.py`, CI files): MIT. See [LICENSE.md](LICENSE.md).
