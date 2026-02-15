import numpy as np

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
        # A = C * (Y * Delta Sigma * sqrt(pi))^m
        A = self.c * (geometry_factor * stress_range * np.sqrt(np.pi)) ** self.m

        if abs(self.m - 2.0) < 1e-9:
            integral = np.log(a_final) - np.log(a_initial)
        else:
            exponent = 1.0 - 0.5 * self.m
            integral = (a_final ** exponent - a_initial ** exponent) / exponent

        return integral / A

    def calculate_crack_growth_rate(self, delta_k):
        """
        Calculates da/dN for a given Delta K.

        Args:
            delta_k (float): Stress Intensity Factor Range (Pa*sqrt(m)).

        Returns:
            float: da/dN (m/cycle).
        """
        return self.c * (delta_k ** self.m)
