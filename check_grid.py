"""Optional finite-grid check of the discrete analogue of the exchangeability theorem.

Requires NumPy and SciPy.  Magnitudes are restricted to m equally spaced point masses
(each with a fair sign), and the pair functional 3*gamma - 2*s*rho (in its sign-magnitude
form) is minimised over all exchangeable laws on n coordinates by linear programming.
The prediction is the discrete analogue of the theorem: zero residual energy for even n,
and a singleton placed on the m/n cells with the smallest values of h_s for odd n.
This tests the extremal mechanism on atomic grids; it does not prove the continuous theorem.
"""
from itertools import combinations_with_replacement
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

TOL = 1e-9


def check_grid(n, m, slopes):
    radii = (np.arange(m) + 0.5) / m
    signs = np.repeat([-1, 1], m)
    magnitudes = np.tile(radii, 2)
    samples = np.array(list(combinations_with_replacement(range(2*m), n)))
    count = len(samples)
    marginal = coo_matrix(
        (np.full(count*n, 1/n), (samples.ravel(), np.repeat(np.arange(count), n))),
        shape=(2*m, count),
    ).tocsc()
    worst = 0.0
    for slope in slopes:
        h = radii - slope*radii**2
        cost = np.zeros(count)
        for i in range(n):
            for j in range(i):
                a, b = samples[:, i], samples[:, j]
                kernel = np.minimum(magnitudes[a], magnitudes[b]) - slope*magnitudes[a]*magnitudes[b]
                cost += 6*signs[a]*signs[b]*kernel
        cost /= n*(n-1)/2
        fit = linprog(cost, A_eq=marginal, b_eq=np.full(2*m, 1/(2*m)), method="highs")
        if not fit.success:
            sys.exit(f"FAILED: LP did not solve ({fit.message})")
        minimum_energy = 6*np.sort(h)[:m//n].mean() if n % 2 else 0.0
        prediction = (minimum_energy - 6*n*h.mean())/(n*(n-1))
        gap = abs(fit.fun - prediction)
        worst = max(worst, gap)
        print(f"n={n} magnitudes={m} s={slope:+.2f} LP={fit.fun:.10f} prediction={prediction:.10f}")
        if gap > TOL:
            sys.exit(f"FAILED: gap {gap:.3e} exceeds tolerance {TOL}")
    return worst


if __name__ == "__main__":
    worst = 0.0
    for n, m in [(3, 6), (4, 4), (5, 5)]:
        worst = max(worst, check_grid(n, m, [-n/2, -1.0, 0.0, 0.8, 0.95, 1.0]))
    print(f"All 18 discrete optima match the predictions (largest gap {worst:.1e}, tolerance {TOL}).")
