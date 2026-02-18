## 2024-05-23 - Root Finding Optimization
**Learning:** For monotonic functions like fracture resistance curves, bracketing methods like the Illinois Algorithm (Regula Falsi with a fix for stagnation) offer a significant speedup (superlinear convergence) over Bisection (linear convergence) while maintaining robustness.
**Action:** Replace simple Bisection implementations with Illinois Algorithm or Brent's Method when optimizing numerical root-finding tasks where function evaluation is expensive.
