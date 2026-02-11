import numpy as np

def j_integral(k_i, youngs_modulus, poisson_ratio=0.3, plane_stress=True):
    """
    Calculates the J-Integral (J) from the Stress Intensity Factor (K_I) for LEFM.

    J = K_I^2 / E'

    Where E' = E (Plane Stress) or E / (1 - v^2) (Plane Strain).

    Args:
        k_i (float): Stress Intensity Factor (Pa*sqrt(m)).
        youngs_modulus (float): Young's Modulus E (Pa).
        poisson_ratio (float): Poisson's Ratio v. Default is 0.3.
        plane_stress (bool): True for Plane Stress, False for Plane Strain.

    Returns:
        float: J-Integral (J/m^2 or N/m).
    """
    if plane_stress:
        effective_modulus = youngs_modulus
    else:
        effective_modulus = youngs_modulus / (1 - poisson_ratio ** 2)

    return k_i ** 2 / effective_modulus

def ctod(k_i, yield_strength, youngs_modulus, constraint_factor=1.0):
    """
    Calculates the Crack Tip Opening Displacement (CTOD).

    delta = K_I^2 / (m * sigma_y * E)

    Args:
        k_i (float): Stress Intensity Factor (Pa*sqrt(m)).
        yield_strength (float): Yield Strength sigma_y (Pa).
        youngs_modulus (float): Young's Modulus E (Pa).
        constraint_factor (float): Constraint factor m. Typically 1.0 - 2.0.

    Returns:
        float: CTOD delta (m).
    """
    return k_i ** 2 / (constraint_factor * yield_strength * youngs_modulus)
