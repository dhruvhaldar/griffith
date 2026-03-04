## 2024-03-24 - Scalar multiplication vs exponentiation
**Learning:** In hot computational paths, replacing `x ** 2` with `x * x` for floating-point numbers yields a ~12% performance improvement. This is particularly relevant in LEFM calculations like `critical_crack_length` where such squaring operations are part of the core mathematical model and are called frequently.
**Action:** When optimizing tight numerical loops or frequently called mathematical functions for scalar values, replace `** 2` with `val * val`. This pattern should be consistently applied alongside the existing `math.sqrt()` vs `** 0.5` optimizations.

## 2024-05-15 - Precompute invariant constants in mathematical simulations
**Learning:** In scientific code mimicking hot paths like `ParisLawIntegrator`, constant multiplications or exponential expressions combining static class properties (`self.c`, `self.m`) with unvarying math constants (like `math.sqrt(math.pi)`) can incur surprising performance penalties when recalculated each loop or call. Distributing exponential terms `(x * c)**m = (x**m) * (c**m)` and precomputing `c**m` yielded a ~17% speedup.
**Action:** When optimizing inner hot paths in simulation or equation classes, look for math operations that only involve initialized constants (e.g. static configuration numbers, math/np constant values) and precompute them in the `__init__` constructor instead of computing inline.

## 2024-06-05 - Pre-calculate scalar terms before array multiplication
**Learning:** When performing operations involving both scalar values and NumPy arrays, grouping the scalar operations and calculating them first before applying them to the array significantly reduces computation time (by ~40%). NumPy array broadcasting overhead for multiple scalar operations is expensive compared to a single pre-calculated scalar value multiplied by the array.
**Action:** Before applying mathematical formulas to NumPy arrays in hot paths (like `RCurveAnalysis.plot_stability_diagram`), pre-calculate all scalar terms into a single constant first.
