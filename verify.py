"""Exact rational checks for "Quadrant dependence, reflected copula measures and exchangeable ranks".

Standard library only. Every check raises SystemExit on failure (no assert statements),
so the script behaves identically under python -O.  Run:  python3 verify.py
"""
from fractions import Fraction as Q
from math import comb


def check(condition, label):
    if not condition:
        raise SystemExit("FAILED: " + label)
    print("ok  " + label)


# ---------------------------------------------------------------------------
# Section 3: explicit parameters for the two polynomial families
# ---------------------------------------------------------------------------
def variance_coefficient(k):
    """V_k = Var_T[(a_k(T)+a_k(1-T))/2] for a_k(x) = x^k - x, T uniform."""
    return Q(1, 2*(2*k+1))*(1+Q(1, comb(2*k, k)))-Q(1, (k+1)**2)


def section3():
    check(24*variance_coefficient(2) == Q(2, 15), "24 V_2 = 2/15")
    slope = 24*(variance_coefficient(2)-2*variance_coefficient(100))
    check(slope > Q(1, 75), "Family B rank slope 24(V_2 - 2 V_100) > 1/75")
    print("    slope =", float(slope))
    # Family B: f = x + x^2 - 2 x^100 ; |f| <= 2, f' in [-199, 3]; |grad A| <= 400
    # arithmetic only: the inputs |f_B| <= 2, f_B' in [-199, 3], |grad A| <= 400 are proved in the text
    remainder = 4*400+4
    check(remainder == 1604, "remainder constant 1604")
    check(48*remainder*Q(1, 10**8) < Q(1, 75), "48*1604*1e-8 < 1/75")
    check(Q(1, 10**8) < Q(1, 197**2), "1e-8 < 197^-2 (global quadrant sign)")
    check(Q(1, 10**8)*(1+4+2*100**2) < 1, "Family B density numerator positive at 1e-8 (d=2)")
    # Family A: f = x - 2x^2 + x^3, explicit folded margin at |eps| <= 1e-3
    eps = Q(1, 1000)
    margin = 9*Q(992, 1000)**2-8*Q(1002, 1000)**2-16*eps*(1+eps)
    check(margin > Q(4, 5), "Family A folded margin > 4/5 at |eps| <= 1e-3")
    # the D_k bounds used in the text
    S_lo, S_hi = 1-2*eps, 1+2*eps          # |S - 1| <= 2|eps|
    p_hi = (S_hi/2)**2                     # p = h l <= (S/2)^2
    D2_hi = 1+eps+3*eps*p_hi
    D3_lo = (1-eps)*S_lo-4*eps*p_hi
    check(D2_hi <= Q(1002, 1000), "D_2 <= 1.002")
    check(D3_lo >= Q(992, 1000), "D_3 >= 0.992")
    check(1-eps*(1+2*4+9) > 0, "Family A density numerator positive at 1e-3 (d=2)")


# ---------------------------------------------------------------------------
# Section 5: three-rate frailty certificate (rates 1, 2, 200, equal weights)
# ---------------------------------------------------------------------------
def folded_density_interval(m=200, steps=34):
    def inverse_interval(u):
        lo, hi = Q(0), Q(1)
        for _ in range(steps):
            mid = (lo+hi)/2
            if mid+mid**2+mid**m < 3*u:
                lo = mid
            else:
                hi = mid
        return lo, hi

    def density_box(X, Y):
        def numerator(x, y):
            return 3*(1+4*x*y+m*m*(x*y)**(m-1))

        def scale(x):
            return 1+2*x+m*x**(m-1)
        a, b = X
        c, d = Y
        return (numerator(a, c)/(scale(b)*scale(d)),
                numerator(b, d)/(scale(a)*scale(c)))

    u, v = Q(2, 5), Q(3, 10)
    X, Y, H, K = map(inverse_interval, (u, v, 1-u, 1-v))
    a, b = density_box(X, Y)
    c, d = density_box(H, K)
    e, f = density_box(X, K)
    g, h = density_box(H, Y)
    return a+c-f-h, b+d-e-g


def section5():
    lo, hi = folded_density_interval()
    check(-Q(653, 100000) < lo <= hi < -Q(652, 100000),
          "rates (1,2,200): folded density at (2/5,3/10) in (-0.00653,-0.00652)")
    # limit argument: y solves y + y^2 = 9/10 and exceeds 1/2
    check(Q(1, 2)+Q(1, 4) < Q(9, 10), "limit root for v = 3/10 exceeds 1/2")


# ---------------------------------------------------------------------------
# Section 6: finite exchangeability, closed forms and exact extremal integration
# ---------------------------------------------------------------------------
def h(s, x):
    return x-s*x*x


def H(s, x):          # antiderivative of h_s (exact)
    x = Q(x)
    return x*x/2-s*x**3/3


def bound(n, s):
    """d_n(s) from the theorem, computed from the sublevel set I_{n,s}."""
    a = 3-2*s
    if n % 2 == 0:
        return -a/(n-1)
    if s <= Q(n, n+1):
        integral = H(s, Q(1, n))
    else:
        b = (Q(1, n)+1/s-1)/2
        c = Q(1, n)-b
        integral = H(s, b)+(H(s, 1)-H(s, 1-c))
    return (6*integral-a)/(n-1)


def closed_form(n, s):
    if n % 2 == 0:
        return -(3-2*s)/(n-1)
    if s <= Q(n, n+1):
        return (2*s*(n*n+n+1)-3*n*(n+1))/Q(n**3)
    return s/(2*n)-3/(2*n*s)-s/Q(n*n)+s/Q(2*n**3)


def kernel(s, u, v):
    """Pair functional 3*gamma - 2*s*rho as an expectation over (U,V)."""
    return 6*(abs(u+v-1)-abs(u-v))-2*s*(12*u*v-3)


def path_pair_integral(s, x, y):
    """E_t kernel(x(t), y(t)) for affine paths x = x0 + x1 t, y = y0 + y1 t, t in [0,1].
    The kernel is piecewise quadratic with breaks where u = v or u + v = 1;
    Simpson's rule is exact on each piece."""
    (a, b), (c, d) = x, y
    knots = {Q(0), Q(1)}
    for intercept, slope in [(a-c, b-d), (a+c-1, b+d)]:
        if slope != 0:
            t = -intercept/slope
            if 0 < t < 1:
                knots.add(t)
    knots = sorted(knots)

    def k(t):
        return kernel(s, a+b*t, c+d*t)
    return sum((hi-lo)*(k(lo)+4*k((lo+hi)/2)+k(hi))/6 for lo, hi in zip(knots, knots[1:]))


def to_u(sign, r0, r1):
    """Coordinate U = (1 + sign*r)/2 for magnitude path r = r0 + r1 t."""
    return (Q(1, 2)+sign*r0/2, sign*r1/2)


def extremal_value(n, s):
    """Exact value of 3*gamma - 2*s*rho for the extremal exchangeable law."""
    def average(paths):
        tot = sum(path_pair_integral(s, x, y)
                  for i, x in enumerate(paths) for j, y in enumerate(paths) if i != j)
        return tot/(n*(n-1))

    if n % 2 == 0:
        pair = [to_u(1, Q(0), Q(1)), to_u(-1, Q(0), Q(1))]
        return average(pair*(n//2))
    if s <= Q(n, n+1):
        pieces = [(Q(1), Q(0), Q(1, n))]          # weight, start, length of I
        lo_J, len_J = Q(1, n), 1-Q(1, n)
    else:
        b = (Q(1, n)+1/s-1)/2
        c = Q(1, n)-b
        pieces = [(n*b, Q(0), b), (n*c, 1-c, c)]
        lo_J, len_J = b, 1-b-c
    pair = [to_u(1, lo_J, len_J), to_u(-1, lo_J, len_J)]*((n-1)//2)
    value = Q(0)
    for weight, start, length in pieces:
        for sign in (1, -1):
            value += weight*Q(1, 2)*average(pair+[to_u(sign, start, length)])
    return value


def section6():
    for n in range(2, 52):
        for s in [Q(-n, 2), Q(-1), Q(-1, 2), Q(0), Q(1, 3), Q(n, n+1), Q(9, 10), Q(1)]:
            if bound(n, s) != closed_form(n, s):
                raise SystemExit(f"FAILED: closed form n={n} s={s}")
    print("ok  closed forms agree with the integral formula, n = 2..51, eight slopes")
    for n in range(3, 52, 2):
        s0 = Q(n, n+1)
        lhs = (2*s0*(n*n+n+1)-3*n*(n+1))/Q(n**3)
        rhs = s0/(2*n)-3/(2*n*s0)-s0/Q(n*n)+s0/Q(2*n**3)
        if lhs != rhs:
            raise SystemExit(f"FAILED: branches disagree at s=n/(n+1), n={n}")
        d1 = 2*(n*n+n+1)/Q(n**3)                       # derivative of branch 1
        d2 = Q(1, 2*n)+3/(2*n*s0*s0)-Q(1, n*n)+Q(1, 2*n**3)
        if d1 != d2:
            raise SystemExit(f"FAILED: derivatives disagree at s=n/(n+1), n={n}")
    print("ok  the two odd branches agree in value and slope at s = n/(n+1), n = 3..51")
    check(bound(3, Q(1)) == -Q(23, 54), "d_3(1) = -23/54")
    check(bound(3, Q(0)) == -Q(4, 3), "d_3(0) = -4/3, so min Gini for n=3 is -4/9")
    check(bound(5, Q(1)) == -Q(59, 250), "d_5(1) = -59/250")
    check(bound(3, Q(3, 4)) == -Q(11, 18), "d_3(3/4) = -11/18")
    for n in range(3, 102, 2):
        if bound(n, Q(1)) != -Q(2*n*n+2*n-1, 2*n**3) or bound(n, Q(0)) != -3*Q(n+1, n*n):
            raise SystemExit(f"FAILED: corollary formulas n={n}")
    print("ok  corollary formulas for s = 1 and s = 0, odd n = 3..101")
    count = 0
    for n in range(2, 10):
        slopes = [Q(-n, 2), Q(-1), Q(0), Q(1, 2), Q(n, n+1), Q(19, 20), Q(1)]
        for s in slopes:
            if extremal_value(n, s) != bound(n, s):
                raise SystemExit(f"FAILED: extremal integration n={n} s={s}")
            count += 1
    print(f"ok  direct integration of the copula kernel matches d_n(s) in {count} cases (n = 2..9)")
    # Remark on s < -n/2: the bound (6*int_0^{1/n} phi_q - a_s)/(n-1) lies strictly below the singleton value
    def phi_integral(q, top):
        knee = 1/(2*q)
        if top <= knee:
            return top*top/2+q*top**3/3
        return knee*knee/2+q*knee**3/3+(top*top-knee*knee)-(top-knee)/(4*q)
    for n, s in [(3, Q(-3)), (3, Q(-6)), (5, Q(-5)), (7, Q(-4))]:
        q = -s
        lower = (6*phi_integral(q, Q(1, n))-(3-2*s))/(n-1)
        singleton = (6*H(s, Q(1, n))-(3-2*s))/(n-1)
        if not lower < singleton:
            raise SystemExit(f"FAILED: remark bound n={n} s={s}")
    print("ok  for s < -n/2 the valid lower bound lies strictly below the singleton value (4 cases)")
    check((6*phi_integral(Q(3), Q(1, 3))-9)/2 == -Q(305, 72), "remark bound at n=3, s=-3 equals -305/72")
    # Section 7: ordinary Gini parity constant J_k = 1/k (integral of 4(1-k+2kp) over [(k-1)/(2k),1/2])
    for k in range(1, 40, 2):
        lo, hi = Q(k-1, 2*k), Q(1, 2)
        J = 4*((1-k)*(hi-lo)+k*(hi*hi-lo*lo))
        if J != Q(1, k):
            raise SystemExit(f"FAILED: J_k for k={k}")
    print("ok  J_k = 1/k for ordinary Gini's gamma, odd k < 40")


if __name__ == "__main__":
    section3()
    section5()
    section6()
    print("All exact checks passed.")
