## 2024-05-23 - Root Finding Optimization
**Learning:** For monotonic functions like fracture resistance curves, bracketing methods like the Illinois Algorithm (Regula Falsi with a fix for stagnation) offer a significant speedup (superlinear convergence) over Bisection (linear convergence) while maintaining robustness.
**Action:** Replace simple Bisection implementations with Illinois Algorithm or Brent's Method when optimizing numerical root-finding tasks where function evaluation is expensive.

## 2025-02-27 - Python Scalar Performance
**Learning:** `math` module is ~4x faster than `numpy` for scalar operations (e.g. `sqrt`), but adding type checks (`isinstance`) to support both scalar and array inputs reduces the gain to ~2x. Given the small absolute difference (microseconds), it's rarely worth sacrificing readability or robustness for this micro-optimization in API handlers.
**Action:** Prefer `numpy` for consistency in libraries that handle both scalars and arrays, unless in a tight loop with guaranteed scalar inputs.
