import numpy as np
from scipy.integrate import quad

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

    def predict_cycles(self, stress_range, a_initial, a_final, geometry_factor=1.0):
        """
        Predicts the number of cycles N to grow a crack from a_initial to a_final.

        N = Integral_{a_i}^{a_f} (1 / (C * (Delta K)^m)) da

        Delta K = Y * Delta Sigma * sqrt(pi * a)

        Args:
            stress_range (float): Delta Sigma (Pa).
            a_initial (float): Initial crack length (m).
            a_final (float): Final crack length (m).
            geometry_factor (float): Geometry factor Y. Assumed constant for simplicity.

        Returns:
            float: Number of cycles N.
        """
        def integrand(a):
            delta_k = geometry_factor * stress_range * np.sqrt(np.pi * a)
            da_dn = self.c * (delta_k ** self.m)
            return 1.0 / da_dn

        result, error = quad(integrand, a_initial, a_final)
        return result

    def calculate_crack_growth_rate(self, delta_k):
        """
        Calculates da/dN for a given Delta K.

        Args:
            delta_k (float): Stress Intensity Factor Range (Pa*sqrt(m)).

        Returns:
            float: da/dN (m/cycle).
        """
        return self.c * (delta_k ** self.m)
