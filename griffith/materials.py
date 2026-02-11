import numpy as np

class Material:
    def __init__(self, name, youngs_modulus, yield_strength, k_ic=None, j_ic=None):
        """
        Args:
            name (str): Material name.
            youngs_modulus (float): E (Pa).
            yield_strength (float): Sigma_y (Pa).
            k_ic (float, optional): Fracture Toughness (Pa*sqrt(m)).
            j_ic (float, optional): Fracture Toughness (J/m^2).
        """
        self.name = name
        self.youngs_modulus = youngs_modulus
        self.yield_strength = yield_strength
        self.k_ic = k_ic
        self.j_ic = j_ic

    def critical_crack_length(self, stress, geometry_factor=1.0):
        """
        Calculates critical crack length based on K_IC.
        """
        if self.k_ic is None:
            raise ValueError(f"K_IC not defined for {self.name}")

        # a_c = (1/pi) * (K_IC / (Y * sigma))^2
        return (1.0 / np.pi) * (self.k_ic / (geometry_factor * stress)) ** 2

class Steel(Material):
    def __init__(self, K_IC=50e6, yield_strength=350e6):
        super().__init__(
            name="Steel",
            youngs_modulus=200e9,
            yield_strength=yield_strength,
            k_ic=K_IC
        )

class Aluminum(Material):
    def __init__(self, K_IC=25e6, yield_strength=300e6):
        super().__init__(
            name="Aluminum 2024-T3",
            youngs_modulus=73e9,
            yield_strength=yield_strength,
            k_ic=K_IC
        )

class Titanium(Material):
    def __init__(self, K_IC=55e6, yield_strength=830e6):
        super().__init__(
            name="Titanium Ti-6Al-4V",
            youngs_modulus=113e9,
            yield_strength=yield_strength,
            k_ic=K_IC
        )
