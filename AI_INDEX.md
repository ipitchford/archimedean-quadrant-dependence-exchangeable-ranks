# AI index: Quadrant dependence, reflected copula measures and exchangeable ranks (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1
states the problem, why it matters, what was known, what is new, the scope and a roadmap).
DOI 10.5281/zenodo.24547093 (concept 10.5281/zenodo.24547092). Status: unrefereed candidate; internal AI-assisted
review and exact computational checks only.

## Notation

C = bivariate copula, Pi = independence copula. PQD: C >= Pi; NQD: C <= Pi. eta_C = reflected measure on (0,1/2)^2
(mass of a rectangle and its point reflection minus its two single reflections); PMI: eta_C >= 0; NMI: eta_C <= 0
(Fuchs-Tschimpke Definition 1). F_c = folded density. rho = Spearman's rho, gamma = Gini's gamma; D_s = 3 gamma -
2 s rho, D = D_1. Archimedean: C(u,v) = psi(psi^-1(u) + psi^-1(v)). n-extendible pair: first two coordinates of an
exchangeable vector of n uniform ranks. d_n(s) = minimum of D_s over n-extendible pairs.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A | Conditionally i.i.d. pairs satisfy 3 gamma - 2 rho = 24 E Var(...) >= 0; strict frailty models: equality only at independence | Lemma 2.1 | written proof; ingredients from Fuchs (2024) Theorem 6 and Corollary 5 |
| B | All four implications PMI=>PQD, NMI=>NQD, NQD=>NMI, PQD=>PMI fail for real-analytic Archimedean copulas with positive densities, arbitrarily close to independence in every C^m norm; explicit ranges 0<|eps|<=1e-3 (f_A) and 0<|eps|<=1e-8 (f_B = x + x^2 - 2x^100); margins of exchangeable Archimedean copulas in every finite dimension d (explicit thresholds); in the PQD example D < 0 | Theorem 3.1; eqs. (5)-(6); Remark 3.2 | written proof; Graham (2026) first refuted PQD=>PMI only; constants checked exactly in verify.py |
| C | The full family of Fuchs-Tschimpke comparisons [C,B] >= [C,A] holds iff the symmetrised reflected measure is nonnegative; for exchangeable C (all Archimedean C) this is PMI; no finite subfamily characterises PMI | Theorem 4.1; Corollary 4.2 | written proof |
| D | Shared frailty: at most two frailty values => PMI; three values (rates 1, 2, m) fail PMI for all large m, certified at m = 200 (-0.00653 < F_c(2/5,3/10) < -0.00652); a failing example can be MTP2 in every dimension and TP of every order | Proposition 5.1; Corollary 5.2 | written proof; Müller-Scarsini MTP2 criterion; certificate in verify.py |
| E | For n-extendible pairs and -n/2 <= s <= 1, D_s ranges exactly over [d_n(s), 3 - 2s]; d_n(s) = -(3-2s)/(n-1) for even n, explicit parity correction for odd n; n = 3: 3 gamma - 2 rho >= -23/54, gamma >= -4/9; d_5(1) = -59/250 | Theorem 6.1; Corollary 6.2 | written proof; sign-magnitude representation of Ansari-Rockel-Steinmaßl Lemma 3.1; closed forms and attainment checked exactly; finite-grid LPs agree |
| F | For s < -n/2 (odd n) a valid lower bound, strictly below the singleton value; n = 3, s = -3: -305/72 | Remark 6.4 | written proof; verify.py |
| G | Generalised Gini's gamma: exact smallest common pairwise value in every dimension n (ordinary Gini, n = 3: -4/9; Koike-Hofert Gaussian example about -0.379; correlation-matrix bound -1/2); J_k = 1/k; integer quadratic inequalities for all attainable matrices | Theorem 7.1 | written proof; Koike-Hofert Theorem 3 representation |

## Evidence

| Check | Program | Output | Arithmetic |
|---|---|---|---|
| Effect-size slopes, remainder constants, density positivity, folded-density margins (Theorem 3.1); 24 V_2 = 2/15; three-rate frailty certificate; closed forms of d_n(s) (n = 2..51), C^1 junction, -23/54, -4/9, -59/250, -11/18; attainment by direct integration in 56 cases; Remark 6.4 bound -305/72; J_k = 1/k | [verify.py](verify.py) | [results/verify.txt](results/verify.txt) | exact rationals (standard library) |
| Discrete analogue of Theorem 6.1: LP optimum over exchangeable laws on atomic grids equals the prediction in 18 cases (largest gap 1.4e-14, tolerance 1e-9) | [check_grid.py](check_grid.py) | [results/check_grid.txt](results/check_grid.txt) | floating LP (SciPy HiGHS); a test of the mechanism, not a proof |

Numbers quoted on the release page: -4/9 and -23/54 (three units); -1/(n-1) (even n, s = 1); one in a thousand and
one in a hundred million (explicit parameters); frailty rates 1, 2 and 200; effect sizes about two in ten billion
(f_B) and about three in a hundred thousand (f_A); Koike-Hofert Gaussian value about -0.379 and correlation bound -1/2.

## Limits

All statements are about populations. The counterexamples are tiny effects (D of order 1e-10 and 1e-5 at the explicit
parameters) and say nothing about the power of tests. No finite-sample test of the exchangeability limits is given.
Open: D_s ranges for s < -n/2 and s > 1 (hence the full attainable (rho, gamma) set for n exchangeable ranks); the full
generalised Gini compatibility sets; which standard Archimedean families are PMI (Section 8).

## Replay and records

Replay commands and comparison policy: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt),
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI [.github/workflows/replay.yml](.github/workflows/replay.yml) with
[.github/ci/compare_outputs.py](.github/ci/compare_outputs.py). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior
art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json). Bibliography: [refs.bib](refs.bib). Licences:
[LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff). Hashes: [MANIFEST.sha256](MANIFEST.sha256).
