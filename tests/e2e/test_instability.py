import pytest
from griffith.materials import Steel

class PressureVessel:
    def __init__(self, radius, thickness, pressure):
        self.radius = radius
        self.thickness = thickness
        self.pressure = pressure

    @property
    def hoop_stress(self):
        # Sigma = P * r / t
        return self.pressure * self.radius / self.thickness

def test_leak_before_break():
    """
    E2E Test: Check if a pressure vessel leaks before it bursts.
    Condition: CriticalCrackLength > WallThickness
    """
    vessel = PressureVessel(radius=1.0, thickness=0.01, pressure=2e6)
    material = Steel(K_IC=80e6) # High toughness

    # Using default geometry factor Y=1.0 (Infinite plate approx)
    a_crit = material.critical_crack_length(stress=vessel.hoop_stress)

    # If critical length > thickness, it leaks first (safe failure)
    assert a_crit > vessel.thickness
