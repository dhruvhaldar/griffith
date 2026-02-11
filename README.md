# Griffith

**Griffith** is a computational fracture mechanics suite designed for **SE2139 Fracture Mechanics**. Named after A.A. Griffith, the father of fracture mechanics, this tool automates the assessment of structural integrity in the presence of defects.

It covers both **Linear Elastic Fracture Mechanics (LEFM)** for brittle materials and **Elastic-Plastic Fracture Mechanics (EPFM)** for ductile metals, providing a rigorous platform for predicting critical loads and remaining useful life.

## 📚 Syllabus Mapping (SE2139)

This project strictly adheres to the course learning outcomes:

| Module | Syllabus Topic | Implemented Features |
| --- | --- | --- |
| **LEFM** | *State of stress near crack front* | Calculation of Stress Intensity Factors (K) and Geometry Factors (Y). |
| **EPFM** | *Crack driving force in nonlinear materials* | **J-Integral** estimation schemes and **CTOD** (Crack Tip Opening Displacement) analysis. |
| **Stability** | *Stable or unstable manner* | **R-Curve** analysis (Driving Force vs Resistance) to determine instability points. |
| **Fatigue** | *Growth of existing cracks* | **Paris Law** integration (da/dN) for life prediction. |
| **Testing** | *Evaluate fracture toughness data* | Tools to reduce data from Compact Tension (CT) and Single Edge Notch Bend (SENB) tests. |

## 🚀 Deployment (Vercel)

Griffith runs as a serverless engineering calculator.

1. **Fork** this repository.
2. Deploy to **Vercel** (Python runtime is auto-detected).
3. Access the **Crack Analyzer** at `https://your-griffith.vercel.app`.

## 📊 Artifacts & Structural Integrity Analysis

### 1. Stress Intensity Factor Calculator (K)

*Calculates the driving force for a crack in a standard geometry, such as a Center Cracked Tension (CCT) specimen.*

**Code:**

```python
from griffith.lefm import StressIntensityFactor
from griffith.geometry import CenterCrackedPlate

# Define Geometry: Width=100mm, Crack Length 2a=20mm
specimen = CenterCrackedPlate(width=0.1, crack_length=0.02)

# Calculate K_I for 200 MPa remote stress
K_I = specimen.calculate_k1(stress=200e6)
print(f"K_I: {K_I/1e6:.2f} MPa√m")

```

**Artifact Output:**

> *Figure 1: Stress Intensity Factor vs. Crack Length. The curve shows the non-linear increase of K as the crack grows. The horizontal line represents the material's Fracture Toughness (K_IC), and the intersection point defines the critical crack length a_c.*

### 2. R-Curve Analysis (Stability)

*Determines whether crack growth will be stable (ductile tearing) or unstable (brittle fracture).*

**Code:**

```python
from griffith.r_curve import RCurveAnalysis

# Material Resistance Curve (J-R curve)
def material_resistance(delta_a):
    return 150 + 400 * (delta_a ** 0.5) # kJ/m^2

# Applied Driving Force (J_applied)
analysis = RCurveAnalysis(resistance_func=material_resistance)
critical_stress = analysis.find_instability_load(initial_crack=0.05)

analysis.plot_stability_diagram()

```

**Artifact Output:**

> *Figure 2: The R-Curve Diagram. The solid line is the material's resistance (R) to cracking. The dashed lines are the applied driving force curves (J or G) at different load levels. Instability occurs at the point of tangency, where dJ/da = dR/da.*

### 3. Fatigue Crack Growth (Paris Law)

*Predicts the number of cycles remaining before a crack reaches critical size.*

**Code:**

```python
from griffith.fatigue import ParisLawIntegrator

# Paris Law Parameters for Steel
C = 1.5e-11
m = 3.0

# Integrate from initial size (2mm) to critical size (20mm)
life = ParisLawIntegrator(C, m).predict_cycles(
    stress_range=150e6,
    a_initial=0.002,
    a_final=0.020,
    geometry_factor=1.12
)

```

**Artifact Output:**

> *Figure 3: Crack Growth Curve (a vs. N). The plot shows the exponential acceleration of crack growth rate as the crack length increases, predicting the remaining useful life of the component.*

## 🧪 Testing Strategy

### Unit Tests (Handbook Solutions)

Located in `tests/unit/`.

*Example: `tests/unit/test_sif.py*`

```python
def test_k1_infinite_plate():
    """
    Verifies K_I = sigma * sqrt(pi * a) for an infinite plate.
    """
    stress = 100e6
    a = 0.01
    expected_k1 = stress * (3.14159 * a) ** 0.5

    # Using a very wide plate to approximate infinite
    plate = CenterCrackedPlate(width=100.0, crack_length=2*a)
    calculated_k1 = plate.calculate_k1(stress)

    assert abs(calculated_k1 - expected_k1) < 1e-3

```

### E2E Tests (Failure Prediction)

Located in `tests/e2e/`.

*Example: `tests/e2e/test_instability.py*`

```python
def test_leak_before_break():
    """
    E2E Test: Check if a pressure vessel leaks before it bursts.
    Condition: 2 * WallThickness < CriticalCrackLength
    """
    vessel = PressureVessel(radius=1.0, thickness=0.01, pressure=2e6)
    material = Steel(K_IC=80e6) # High toughness

    a_crit = material.critical_crack_length(stress=vessel.hoop_stress)

    # If critical length > thickness, it leaks first (safe failure)
    assert a_crit > vessel.thickness

```

## ⚖️ License

**MIT License**

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files... [Standard MIT Text]
