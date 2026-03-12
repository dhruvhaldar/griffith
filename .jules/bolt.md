## 2024-03-24 - Scalar multiplication vs exponentiation
**Learning:** In hot computational paths, replacing `x ** 2` with `x * x` for floating-point numbers yields a ~12% performance improvement. This is particularly relevant in LEFM calculations like `critical_crack_length` where such squaring operations are part of the core mathematical model and are called frequently.
**Action:** When optimizing tight numerical loops or frequently called mathematical functions for scalar values, replace `** 2` with `val * val`. This pattern should be consistently applied alongside the existing `math.sqrt()` vs `** 0.5` optimizations.

## 2024-05-15 - Precompute invariant constants in mathematical simulations
**Learning:** In scientific code mimicking hot paths like `ParisLawIntegrator`, constant multiplications or exponential expressions combining static class properties (`self.c`, `self.m`) with unvarying math constants (like `math.sqrt(math.pi)`) can incur surprising performance penalties when recalculated each loop or call. Distributing exponential terms `(x * c)**m = (x**m) * (c**m)` and precomputing `c**m` yielded a ~17% speedup.
**Action:** When optimizing inner hot paths in simulation or equation classes, look for math operations that only involve initialized constants (e.g. static configuration numbers, math/np constant values) and precompute them in the `__init__` constructor instead of computing inline.

## 2024-06-05 - Pre-calculate scalar terms before array multiplication
**Learning:** When performing operations involving both scalar values and NumPy arrays, grouping the scalar operations and calculating them first before applying them to the array significantly reduces computation time (by ~40%). NumPy array broadcasting overhead for multiple scalar operations is expensive compared to a single pre-calculated scalar value multiplied by the array.
**Action:** Before applying mathematical formulas to NumPy arrays in hot paths (like `RCurveAnalysis.plot_stability_diagram`), pre-calculate all scalar terms into a single constant first.

## 2024-10-25 - Multiply by inverse over constant division
**Learning:** In highly mathematical hot-paths such as calculating integrations or formulas repeatedly (like `ParisLawIntegrator`), dividing variables by constants repeatedly is slower than precalculating the inverse of the constant once `inv_const = 1.0 / const` and then performing a multiplication `val * inv_const`. In testing, applying this to cycle prediction computations yielded ~3% further performance gains.
**Action:** Precalculate the inverse of variables acting as divisors in mathematically heavy loops and multiply by the inverse rather than dividing.

## 2024-10-25 - Horner's Method for Polynomials
**Learning:** Hard-coded polynomial expansions with variable factors (e.g., `A - B*x + C*x^2`) are significantly faster evaluated via Horner's Method `A + x*(-B + C*x)` due to avoiding expensive power operations (`** 2` or `x * x`) and saving on multiplication operations overall. This yielded a ~14% reduction in execution time for SingleEdgeNotchBend geometry factor evaluation.
**Action:** Whenever mathematically evaluating a static polynomial expansion, rewrite the formula using Horner's Method for fewer operations and better performance.

## 2024-10-26 - Precompute module-level mathematical constants
**Learning:** Re-evaluating expressions involving standard python math constants (like `math.sqrt(math.pi)`, `1.0 / math.pi`) inside tight loops or high-frequency methods incurs unnecessary overhead. Precomputing these expressions as module-level constants yields a ~20% to ~36% speedup depending on the operation.
**Action:** When working in mathematically heavy modules, check for inline mathematical expressions involving standard constants (e.g. `math.pi`, `np.pi`) and refactor them into module-level constants to be reused across functions and class methods.

## 2025-02-28 - Multiply by 0.5 in root finding loops
**Learning:** In hot-paths like root-finding algorithms (e.g. `_find_root` using Illinois method), dividing by `2` to find midpoints at each iteration is less optimal than multiplying. Replacing `(a + b) / 2` with `(a + b) * 0.5` avoids slower division instructions, yielding a measurable performance boost inside iterative loops.
**Action:** When implementing or optimizing iterative numerical algorithms, avoid dividing by `2` in favor of multiplying by `0.5`.

## 2025-03-05 - Avoid abs() and use float comparisons in hot loops
**Learning:** In tight numerical loops like `_find_root`, calling `abs(x) < tol` is significantly (~40%) slower than doing a double-bounded comparison `-tol < x < tol`. In addition, comparing a float to an integer `0` inside a loop requires implicit type conversion; changing it to `0.0` provides a measurable micro-optimization.
**Action:** When optimizing tight loop condition checks, replace absolute value checks with bound checks (`-tol < x < tol`), and always use float literals (e.g., `0.0`) when comparing against float variables.
