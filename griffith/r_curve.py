import numpy as np
import matplotlib.pyplot as plt

class RCurveAnalysis:
    """
    R-Curve Analysis for stability prediction.
    """
    def __init__(self, resistance_func):
        """
        Args:
            resistance_func (callable): Function R(delta_a) -> resistance (J/m^2 or K units).
        """
        self.resistance_func = resistance_func
        self.critical_values = {}

    def find_instability_load(self, initial_crack, youngs_modulus=200e9, geometry_factor=1.0):
        """
        Finds the critical stress for instability using J-integral approach.

        Assuming R-Curve is in Energy units (J/m^2).

        Instability condition:
        1. J_applied = R
        2. dJ_applied/da = dR/da

        For infinite plate (or simplified): J = (Y * sigma)^2 * pi * a / E

        dJ/da = (Y * sigma)^2 * pi / E  (assuming Y is approx constant for small growth)
        dR/da = d/da (resistance_func(delta_a))

        From 2: (Y * sigma)^2 = (E / pi) * dR/da
        Substitute into 1:
        (E / pi * dR/da) * pi * a / E = R
        a * dR/da = R
        (initial_crack + delta_a) * dR/da = R(delta_a)

        We solve this equation for delta_a_crit.
        """

        # Numerical solution to find delta_a where (a0 + da) * dR/da = R(da)
        delta_a_vals = np.linspace(1e-5, 0.1, 1000) # Sweep 0 to 100mm growth

        lhs = []
        rhs = []

        for da in delta_a_vals:
            # Calculate R
            r_val = self.resistance_func(da)

            # Calculate dR/da numerically
            epsilon = 1e-6
            r_plus = self.resistance_func(da + epsilon)
            r_minus = self.resistance_func(da - epsilon)
            dr_da = (r_plus - r_minus) / (2 * epsilon)

            # Equation: (a0 + da) * dR/da = R
            term = (initial_crack + da) * dr_da

            lhs.append(term)
            rhs.append(r_val)

        # Find intersection
        lhs = np.array(lhs)
        rhs = np.array(rhs)

        # We look for where LHS - RHS crosses zero
        diff = lhs - rhs

        # Find index where sign changes
        idx = np.where(np.diff(np.sign(diff)))[0]

        if len(idx) == 0:
            # Fallback if no intersection found (monotonic rising R-curve without tangency in range)
            return None

        crit_idx = idx[0]
        delta_a_crit = delta_a_vals[crit_idx]
        r_crit = rhs[crit_idx]

        a_crit = initial_crack + delta_a_crit

        # Calculate critical stress from J_applied = R_crit
        # J = Y^2 * sigma^2 * pi * a / E
        # sigma^2 = J * E / (Y^2 * pi * a)

        sigma_c = np.sqrt(r_crit * youngs_modulus / (geometry_factor**2 * np.pi * a_crit))

        self.critical_values = {
            'delta_a': delta_a_crit,
            'a_crit': a_crit,
            'r_crit': r_crit,
            'sigma_c': sigma_c,
            'initial_crack': initial_crack,
            'youngs_modulus': youngs_modulus,
            'geometry_factor': geometry_factor
        }

        return sigma_c

    def plot_stability_diagram(self):
        """
        Plots the R-Curve and Driving Force curves.
        """
        if not self.critical_values:
            print("Run find_instability_load first.")
            return

        cv = self.critical_values
        delta_a = np.linspace(0, cv['delta_a'] * 2, 100)

        # R-Curve
        r_curve = [self.resistance_func(da) for da in delta_a]

        # Driving Force Curve at Critical Stress
        # J_app = (Y * sigma_c)^2 * pi * (a0 + da) / E
        sigma_c = cv['sigma_c']
        a0 = cv['initial_crack']
        E = cv['youngs_modulus']
        Y = cv['geometry_factor']

        j_applied = [(Y * sigma_c)**2 * np.pi * (a0 + da) / E for da in delta_a]

        plt.figure(figsize=(8, 6))
        plt.plot(delta_a * 1000, r_curve, label='Material Resistance (R-Curve)', linewidth=2)
        plt.plot(delta_a * 1000, j_applied, '--', label=f'Applied Driving Force @ {sigma_c/1e6:.1f} MPa')

        plt.scatter([cv['delta_a']*1000], [cv['r_crit']], color='red', zorder=5, label='Instability Point')

        plt.xlabel(r'Crack Extension $\Delta a$ (mm)')
        plt.ylabel(r'J-Integral ($kJ/m^2$ or $N/m$)')
        plt.title('R-Curve Stability Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
