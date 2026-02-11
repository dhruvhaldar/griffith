import pytest
import numpy as np
from griffith.geometry import CenterCrackedPlate
from griffith.lefm import StressIntensityFactor

def test_k1_infinite_plate():
    """
    Verifies K_I = sigma * sqrt(pi * a) for an infinite plate.
    Using a very wide plate to approximate infinite.
    """
    stress = 100e6
    a = 0.01 # Crack length 2a = 0.02
    expected_k1 = stress * np.sqrt(np.pi * a)

    # Using a very wide plate to approximate infinite
    # Width = 100m, Crack = 0.02m. ratio -> 0.
    plate = CenterCrackedPlate(width=100.0, crack_length=2*a)
    calculated_k1 = plate.calculate_k1(stress)

    # Should be close
    assert abs(calculated_k1 - expected_k1) / expected_k1 < 1e-3

def test_critical_crack_length():
    """
    Verifies critical crack length calculation.
    """
    k_ic = 50e6
    stress = 200e6
    Y = 1.0

    expected_a_c = (1 / np.pi) * (k_ic / (Y * stress)) ** 2

    calc_a_c = StressIntensityFactor.critical_crack_length(k_ic, stress, Y)

    assert abs(calc_a_c - expected_a_c) < 1e-5
