import numpy as np

class StressIntensityFactor:
    """
    Base class for Stress Intensity Factor (SIF) calculations.
    """
    def __init__(self, geometry_factor=1.0):
        self.geometry_factor = geometry_factor

    def calculate_k1(self, stress, crack_length):
        """
        Calculates Mode I Stress Intensity Factor (K_I).

        K_I = Y * sigma * sqrt(pi * a)

        Args:
            stress (float): Applied remote stress (Pa).
            crack_length (float): Crack length 'a' (m).

        Returns:
            float: K_I (Pa*sqrt(m)).
        """
        return self.geometry_factor * stress * np.sqrt(np.pi * crack_length)

    @staticmethod
    def critical_crack_length(k_ic, stress, geometry_factor=1.0):
        """
        Calculates the critical crack length for a given fracture toughness.

        a_c = (1/pi) * (K_IC / (Y * sigma))^2

        Args:
            k_ic (float): Fracture toughness (Pa*sqrt(m)).
            stress (float): Applied remote stress (Pa).
            geometry_factor (float): Geometry factor Y (dimensionless).

        Returns:
            float: Critical crack length a_c (m).
        """
        return (1.0 / np.pi) * (k_ic / (geometry_factor * stress)) ** 2
