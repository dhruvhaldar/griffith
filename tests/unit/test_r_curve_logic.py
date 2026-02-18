
import pytest
import numpy as np
from unittest.mock import MagicMock
from griffith.r_curve import RCurveAnalysis

def test_find_instability_load_calls():
    # Define a simple R-Curve and its derivative
    # R = 150 + 400 * sqrt(da) (kJ/m^2)
    def resistance_func(delta_a):
        return (150 + 400 * (delta_a ** 0.5)) * 1000

    def resistance_deriv_func(delta_a):
        return (200 / (delta_a ** 0.5)) * 1000

    # Wrap them in MagicMock to count calls
    mock_r_func = MagicMock(side_effect=resistance_func)
    mock_dr_func = MagicMock(side_effect=resistance_deriv_func)

    analysis = RCurveAnalysis(
        resistance_func=mock_r_func,
        resistance_deriv_func=mock_dr_func
    )

    # Run find_instability_load
    initial_crack = 0.05
    youngs_modulus = 200e9
    geometry_factor = 1.0

    critical_stress = analysis.find_instability_load(
        initial_crack=initial_crack,
        youngs_modulus=youngs_modulus,
        geometry_factor=geometry_factor
    )

    assert critical_stress is not None
    assert critical_stress > 0

    # With Bisection (tol=1e-9, range 1e-5 to 0.1), we expect ~27 iterations.
    # Plus 2 initial calls. Total ~29 calls.
    print(f"Resistance function calls: {mock_r_func.call_count}")

    # We store the call count to verify reduction later
    # For now, just assert it works
    assert mock_r_func.call_count > 0

def test_find_instability_load_correctness():
    # Test a case where we know the analytical solution or approximate it
    # R = A * da^0.5
    # dR/da = 0.5 * A * da^-0.5
    # Target: (a0 + da) * dR/da = R
    # (a0 + da) * 0.5 * A * da^-0.5 = A * da^0.5
    # 0.5 * (a0 + da) = da
    # 0.5 * a0 + 0.5 * da = da
    # 0.5 * a0 = 0.5 * da
    # da = a0

    # So critical extension should be exactly initial_crack if R is purely square root.

    def resistance_func(delta_a):
        return 1000 * (delta_a ** 0.5)

    def resistance_deriv_func(delta_a):
        return 500 * (delta_a ** -0.5)

    analysis = RCurveAnalysis(
        resistance_func=resistance_func,
        resistance_deriv_func=resistance_deriv_func
    )

    initial_crack = 0.02

    critical_stress = analysis.find_instability_load(
        initial_crack=initial_crack,
        youngs_modulus=200e9,
        geometry_factor=1.0
    )

    delta_a_crit = analysis.critical_values['delta_a']

    # We expect delta_a_crit to be close to initial_crack (0.02)
    assert abs(delta_a_crit - initial_crack) < 1e-5
