import numpy as np
import math
from functools import lru_cache
from griffith.lefm import StressIntensityFactor

@lru_cache(maxsize=128)
def _calculate_cct_y_scalar(crack_length, width):
    """
    Cached calculation for scalar inputs.
    """
    alpha = crack_length / width
    return math.sqrt(1 / math.cos(math.pi * alpha / 2))

class CenterCrackedPlate(StressIntensityFactor):
    """
    Center Cracked Plate (CCT) geometry.
    """
    def __init__(self, width, crack_length):
        """
        Args:
            width (float): Plate width W (m).
            crack_length (float): Total crack length 2a (m).
        """
        self.width = width
        self.crack_length = crack_length # 2a
        self._last_calc_crack_length = crack_length
        # Initial Y calculation based on current crack length
        super().__init__(self._calculate_geometry_factor(crack_length))

    def _calculate_geometry_factor(self, crack_length_2a):
        """
        Calculates Y for CCT.

        alpha = a / (W/2) = 2a / W
        Y = sqrt(sec(pi * a / W)) (Approximation)
        """
        if isinstance(crack_length_2a, (int, float)):
            return _calculate_cct_y_scalar(crack_length_2a, self.width)

        alpha = crack_length_2a / self.width
        # Tada, Paris, Irwin formula for finite width correction
        # Y = sqrt(sec(pi * alpha / 2))
        return np.sqrt(1 / np.cos(np.pi * alpha / 2))

    def calculate_k1(self, stress, crack_length=None):
        """
        Calculates K_I for CCT.

        Args:
            stress (float): Remote tensile stress (Pa).
            crack_length (float, optional): Total crack length 2a (m). Defaults to self.crack_length.
        """
        if crack_length is None:
            crack_length = self.crack_length

        # Update geometry factor for the specific crack length only if needed
        # Optimize primarily for scalars (API usage)
        should_calculate = True

        if isinstance(crack_length, (int, float)):
             # Only check cache for scalars
             if (isinstance(self._last_calc_crack_length, (int, float)) and
                 abs(crack_length - self._last_calc_crack_length) < 1e-12):
                 should_calculate = False

        if should_calculate:
            self.geometry_factor = self._calculate_geometry_factor(crack_length)
            if isinstance(crack_length, (int, float)):
                self._last_calc_crack_length = crack_length
            else:
                # Invalidate cache for array inputs or other types
                self._last_calc_crack_length = None

        # For CCT, the formula is usually K = Y * sigma * sqrt(pi * a)
        # where a is half crack length.
        a = crack_length / 2.0
        return super().calculate_k1(stress, a)


class SingleEdgeNotchBend(StressIntensityFactor):
    """
    Single Edge Notch Bend (SENB) specimen.
    """
    def __init__(self, width, thickness, crack_length, span):
        """
        Args:
            width (float): Specimen width W (depth) (m).
            thickness (float): Specimen thickness B (m).
            crack_length (float): Crack length a (m).
            span (float): Support span S (m).
        """
        self.width = width
        self.thickness = thickness
        self.crack_length = crack_length
        self.span = span
        # Initial Y calculation
        super().__init__(self._calculate_f(crack_length))

    def _calculate_f(self, a):
        """
        Calculates f(a/W) for SENB.
        """
        alpha = a / self.width
        # Standard ASTM E399 formula

        if isinstance(a, (int, float)):
            numerator = 3 * math.sqrt(alpha) * (1.99 - alpha * (1 - alpha) * (2.15 - 3.93 * alpha + 2.7 * alpha**2))
            denominator = 2 * (1 + 2 * alpha) * (1 - alpha)**1.5
            return numerator / denominator

        numerator = 3 * np.sqrt(alpha) * (1.99 - alpha * (1 - alpha) * (2.15 - 3.93 * alpha + 2.7 * alpha**2))
        denominator = 2 * (1 + 2 * alpha) * (1 - alpha)**1.5
        return numerator / denominator

    def calculate_k1_from_load(self, load, crack_length=None):
        """
        Calculates K_I based on Load P.

        K_I = (P * S / (B * W^1.5)) * f(a/W)
        """
        if crack_length is None:
            crack_length = self.crack_length

        f_val = self._calculate_f(crack_length)

        return (load * self.span / (self.thickness * self.width ** 1.5)) * f_val

    def calculate_k1(self, stress, crack_length=None):
        """
        Not directly applicable for SENB with 'stress' unless stress represents
        something specific.
        """
        raise NotImplementedError("Use calculate_k1_from_load for SENB geometry.")
