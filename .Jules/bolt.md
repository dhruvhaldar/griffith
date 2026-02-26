## 2024-05-23 - Root Finding Optimization
**Learning:** For monotonic functions like fracture resistance curves, bracketing methods like the Illinois Algorithm (Regula Falsi with a fix for stagnation) offer a significant speedup (superlinear convergence) over Bisection (linear convergence) while maintaining robustness.
**Action:** Replace simple Bisection implementations with Illinois Algorithm or Brent's Method when optimizing numerical root-finding tasks where function evaluation is expensive.

## 2025-02-27 - Python Scalar Performance
**Learning:** `math` module is ~4x faster than `numpy` for scalar operations (e.g. `sqrt`), but adding type checks (`isinstance`) to support both scalar and array inputs reduces the gain to ~2x. Given the small absolute difference (microseconds), it's rarely worth sacrificing readability or robustness for this micro-optimization in API handlers.
**Action:** Prefer `numpy` for consistency in libraries that handle both scalars and arrays, unless in a tight loop with guaranteed scalar inputs.

## 2026-03-05 - Lazy Import Win
**Learning:** `matplotlib.pyplot` is a heavy dependency that significantly increases module import time (~0.7s), causing cold start delays in serverless functions even for endpoints that don't use plotting. Lazy loading it inside the plotting function reduced module import time to ~0.12s.
**Action:** Audit top-level imports in API-critical code for heavy libraries (like `matplotlib`, `pandas`, `scipy.stats`) and lazy load them if they are only used in specific, less-frequent paths.

## 2026-03-05 - Logarithm Optimization
**Learning:** In fatigue calculations (Paris Law integration), calculating `log(a) - log(b)` is mathematically equivalent to `log(a/b)` but requires two expensive log calls instead of one.
**Action:** Always prefer `log(a/b)` over `log(a) - log(b)` in performance-critical numerical integration loops, yielding ~35-45% speedup for that specific operation.
