import pytest
import numpy as np
from griffith.fatigue import ParisLawIntegrator

def test_paris_law_integration():
    """
    Verifies Paris Law integration.
    da/dN = C * (dK)^m
    dK = Y * S * sqrt(pi * a)

    If m=2, Y=1, S=1, C=1, pi=1 (simplified)
    da/dN = a
    int (1/a) da = int dN
    ln(af/ai) = N
    """
    # Using real implementation values
    c = 1e-11
    m = 2.0
    stress_range = 100e6
    a_i = 0.01
    a_f = 0.02
    Y = 1.0

    integrator = ParisLawIntegrator(c, m)
    cycles = integrator.predict_cycles(stress_range, a_i, a_f, Y)

    # Analytical solution for m=2
    # N = (1 / (C * (Y * S * sqrt(pi))^2)) * ln(af/ai)
    # N = (1 / (C * Y^2 * S^2 * pi)) * ln(af/ai)
    expected_cycles = (1.0 / (c * (Y * stress_range)**2 * np.pi)) * np.log(a_f / a_i)

    assert abs(cycles - expected_cycles) / expected_cycles < 1e-3

def test_paris_law_m_neq_2():
    """
    Test for m != 2.
    da/dN = C * (Y * S * sqrt(pi * a))^m = C * (Y S sqrt(pi))^m * a^(m/2)
    N = int_{ai}^{af} a^(-m/2) / (C * (Y S sqrt(pi))^m) da
    N = [ a^(1-m/2) / (1-m/2) ]_{ai}^{af} * (1 / (C * (Y S sqrt(pi))^m))
    """
    c = 1e-11
    m = 3.0
    stress_range = 100e6
    a_i = 0.01
    a_f = 0.02
    Y = 1.0

    integrator = ParisLawIntegrator(c, m)
    cycles = integrator.predict_cycles(stress_range, a_i, a_f, Y)

    term = (c * (Y * stress_range * np.sqrt(np.pi))**m)
    # Integral of a^-1.5 is a^-0.5 / -0.5 = -2 / sqrt(a)
    integral_val = (-2 / np.sqrt(a_f)) - (-2 / np.sqrt(a_i))

    expected_cycles = integral_val / term

    assert abs(cycles - expected_cycles) / expected_cycles < 1e-3
