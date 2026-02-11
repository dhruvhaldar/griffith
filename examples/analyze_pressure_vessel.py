from griffith.materials import Steel

class PressureVessel:
    """
    Simple cylindrical pressure vessel model.
    """
    def __init__(self, radius, thickness, pressure):
        self.radius = radius
        self.thickness = thickness
        self.pressure = pressure

    @property
    def hoop_stress(self):
        # Sigma = P * r / t
        return self.pressure * self.radius / self.thickness

def main():
    """
    LBB (Leak-Before-Break) analysis example.
    """
    # Define Vessel
    # Radius 1.0m, Thickness 10mm, Pressure 2 MPa
    vessel = PressureVessel(radius=1.0, thickness=0.01, pressure=2e6)

    # Define Material (High Toughness Steel)
    material = Steel(K_IC=80e6)

    print(f"Hoop Stress: {vessel.hoop_stress/1e6:.2f} MPa")

    # Calculate Critical Crack Length
    # Assuming infinite plate approximation for small crack vs vessel size
    # Or using a specific geometry factor for cylinder.
    # For now, default Y=1.0 is used (approx).
    a_crit = material.critical_crack_length(stress=vessel.hoop_stress)

    print(f"Critical Crack Length (half-length a): {a_crit*1000:.2f} mm")
    print(f"Total Critical Crack Length (2a): {2*a_crit*1000:.2f} mm")
    print(f"Wall Thickness: {vessel.thickness*1000:.2f} mm")

    # Check LBB
    # Condition: 2a_crit > t (for leak before unstable fracture)
    # Actually, usually if 2a_crit > t, then a through-wall crack is stable.
    # If the critical crack length for SURFACE crack (depth a_crit) > t, then it leaks before break.

    if a_crit > vessel.thickness:
        print("Result: Leak-Before-Break satisfied (Safe).")
    else:
        print("Result: Break-Before-Leak (Unsafe).")

if __name__ == "__main__":
    main()
