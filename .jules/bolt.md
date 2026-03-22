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

## 2025-03-05 - Native ** over math.pow()
**Learning:** Contrary to some assumptions, for floating-point exponentiation in Python, the native `**` operator is roughly ~15% faster than calling the C-backed `math.pow()`, largely because it avoids the overhead of a function call and C-API bindings.
**Action:** When evaluating scalar exponents inside tight mathematical loops, prefer the native `**` operator over `math.pow()`.

## 2025-03-05 - The trap of type() vs isinstance() optimization
**Learning:** While replacing `isinstance(val, (int, float))` with `type(val) in (int, float)` might appear faster in micro-benchmarks (~20% speedup), it prevents type inheritance. This breaks critical logic in scientific codebases where numpy scalars (`np.float64`) are passed, causing them to silently fail the type check and fall back to slower, generic array-processing code.
**Action:** Always prefer `isinstance` over explicit `type()` checks when determining if a variable is a scalar to correctly support scalar types from standard numeric libraries like numpy.

## 2025-03-05 - Redundant inverse multiplication in single-use variables
**Learning:** While `inv_const = 1.0 / const` followed by `val * inv_const` is faster inside a loop where `const` is fixed and `val` changes, pre-calculating the inverse for a single subsequent multiplication (e.g., `inv_A = 1.0 / A; return integral * inv_A`) is a de-optimization. It replaces a single division with both a division and a multiplication.
**Action:** Only precalculate inverse variables (`1.0 / X`) for multiplication if they will be multiplied against multiple different values (e.g. inside a loop). For single-use expressions, directly dividing (`val / X`) is more efficient.

## 2025-03-06 - Group constant calculations to avoid chained division overhead
**Learning:** Evaluating chained divisions or formulas of the form `a / (b / c)` is slower than combining the terms explicitly `a * (c / b)` before division. Grouping scalar math operations in the denominator before evaluating the division ensures the Python interpreter doesn't repeatedly process fraction-based divisions and results in significant (~35%) speedups for scalar mathematical evaluation operations in core hot paths.
**Action:** Always group denominator terms and evaluate division/multiplication before a single overall multiplication/division operation instead of keeping operations separated natively, especially in frequently run mathematical modules.

## 2025-03-16 - Zero measurable impact of float literals over ints in math logic
**Learning:** In Python, converting integer literals (like `3`) to float literals (like `3.0`) in the hopes of avoiding implicit type conversion overhead during arithmetic evaluation is a micro-optimization that yields absolutely zero measurable performance benefit due to the overarching execution overhead of the Python interpreter.
**Action:** Do not sacrifice code readability to enforce float literals inside mathematical expressions, as this is a premature micro-optimization that produces no meaningful speedup.

## 2025-03-16 - Division by 2.0 vs multiplication by 0.5 in isolated scalar evaluations
**Learning:** In Python, replacing an isolated division by a constant (e.g., `a / 2.0`) with multiplication by its decimal equivalent (`a * 0.5`) in a function that is not part of a tight iterative loop yields zero measurable performance benefit. The Python interpreter overhead overshadows the microscopic instruction-level savings.
**Action:** Only apply `* 0.5` over `/ 2.0` in inner iterative loops (like root-finding algorithms). Do not apply it to standalone scalar mathematical assignments where it provides no measurable impact.
## 2025-03-19 - Save a multiplication operation in Regula Falsi
**Learning:** In the root finding hot path `_find_root` using Regula Falsi or Illinois algorithm, replacing the standard calculation `c = (a * fb - b * fa) / (fb - fa)` with `c = a + fa * (a - b) / (fb - fa)` algebraically achieves exactly the same result but avoids one floating point multiplication. Timing analysis confirms this formulation runs ~15% faster.
**Action:** Always use the `c = a + fa * (a - b) / (fb - fa)` formulation when implementing root finding algorithms to save a multiplication operation and improve performance in hot paths.

## 2025-03-20 - Evaluate constant division before evaluation
**Learning:** In formulas that use `1.0 / (2.0 * x)` (like calculating a numerical derivative), Python spends extra evaluation time evaluating the `1.0 / 2.0` portion of the fraction at runtime. Replacing the constant fraction with its literal evaluation `0.5 / x` yielded a ~30% faster execution time for that expression because it saves arithmetic operations.
**Action:** When evaluating equations with constant divisions like `1.0 / (2.0 * var)`, replace the constant fractions with a precalculated float (e.g., `0.5 / var`) to save execution time in heavily used math functions.

## 2025-03-22 - Pre-calculate inverse factors for NumPy arrays
**Learning:** In purely computational functions handling standard scalar constants (like `poisson_ratio`, `yield_strength`) against a large NumPy array input (`k_i`), executing the standard division formulation `(array / (scalar1 * scalar2))` incurs significant broadcast overhead for the division. Converting the scalar denominator to a pre-calculated inverse factor (`factor = 1.0 / (scalar1 * scalar2)`) and multiplying the array `(array * factor)` yields a roughly 25-30% performance speedup when dealing with large arrays.
**Action:** Always pre-calculate scalar denominators into a single inverse multiplicative factor before applying it to NumPy arrays in heavily computed functions like `j_integral` or `ctod`.
