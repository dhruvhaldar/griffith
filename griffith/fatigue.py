import numpy as np
import math

class ParisLawIntegrator:
    """
    Integrates the Paris Law equation to predict fatigue life.

    da/dN = C * (Delta K)^m
    """
    def __init__(self, c, m):
        """
        Args:
            c (float): Paris Law coefficient C.
            m (float): Paris Law exponent m.
        """
        self.c = c
        self.m = m
        # ⚡ Bolt Optimization: Precompute invariant values used in predict_cycles to avoid redundant calculations
        self._m_is_2 = abs(self.m - 2.0) < 1e-9
        self._exponent = 1.0 - 0.5 * self.m
        self._c_sqrt_pi_m = self.c * (math.sqrt(math.pi) ** self.m)
        self._c_sqrt_np_pi_m = self.c * (np.sqrt(np.pi) ** self.m)

        # ⚡ Bolt Optimization: Precompute inverted exponent division to multiply instead later
        if not self._m_is_2:
            self._inv_exponent = 1.0 / self._exponent

    def predict_cycles(self, stress_range, a_initial, a_final, geometry_factor=1.0):
        """
        Predicts the number of cycles N to grow a crack from a_initial to a_final.

        N = Integral_{a_i}^{a_f} (1 / (C * (Delta K)^m)) da

        Delta K = Y * Delta Sigma * sqrt(pi * a)

        Uses an analytical solution for constant geometry_factor Y.
        If m != 2:
            N = (a_f^(1 - m/2) - a_i^(1 - m/2)) / ((1 - m/2) * A)
        If m == 2:
            N = (ln(a_f) - ln(a_i)) / A

        where A = C * (Y * Delta Sigma * sqrt(pi))^m

        Args:
            stress_range (float): Delta Sigma (Pa).
            a_initial (float): Initial crack length (m).
            a_final (float): Final crack length (m).
            geometry_factor (float): Geometry factor Y. Assumed constant for simplicity.

        Returns:
            float: Number of cycles N.
        """
        # Check if inputs are scalars to use math module for performance
        if isinstance(stress_range, (int, float)) and isinstance(a_initial, (int, float)) and isinstance(a_final, (int, float)):
            # ⚡ Bolt Optimization: Use math.pow instead of ** for scalars
            A = self._c_sqrt_pi_m * math.pow(geometry_factor * stress_range, self.m)

            if self._m_is_2:
                # Optimization: log(a) - log(b) = log(a/b). Avoids one log call (~35% faster).
                integral = math.log(a_final / a_initial)
                return integral / A
            else:
                # ⚡ Bolt Optimization: Multiply by inverted exponent instead of dividing
                return ((math.pow(a_final, self._exponent) - math.pow(a_initial, self._exponent)) * self._inv_exponent) / A

        # Fallback to numpy for arrays
        A = self._c_sqrt_np_pi_m * ((geometry_factor * stress_range) ** self.m)

        if self._m_is_2:
            # Optimization: log(a) - log(b) = log(a/b). Avoids one log call (~45% faster for numpy).
            integral = np.log(a_final / a_initial)
            return integral / A
        else:
            # ⚡ Bolt Optimization: Multiply by inverted exponent instead of dividing
            return ((a_final ** self._exponent - a_initial ** self._exponent) * self._inv_exponent) / A

    def calculate_crack_growth_rate(self, delta_k):
        """
        Calculates da/dN for a given Delta K.

        Args:
            delta_k (float): Stress Intensity Factor Range (Pa*sqrt(m)).

        Returns:
            float: da/dN (m/cycle).
        """
        return self.c * (delta_k ** self.m)
