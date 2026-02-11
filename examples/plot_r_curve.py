from griffith.r_curve import RCurveAnalysis
import matplotlib.pyplot as plt

def main():
    # Material Resistance Curve (J-R curve)
    # R = 150 + 400 * (delta_a ** 0.5) # kJ/m^2
    # Note: If output is kJ/m^2, we should probably work in consistent units (e.g., J/m^2).
    # 150 kJ/m^2 = 150,000 J/m^2

    def material_resistance(delta_a):
        # Returns J/m^2
        # delta_a in meters
        # 150 kJ/m^2 = 150,000 J/m^2
        # 400 kJ/m^2/m^0.5 ?? The example: 150 + 400 * sqrt(da)
        # If da is meters, say da=0.01 (10mm), sqrt(da)=0.1. 400*0.1 = 40. Total 190.
        # So units seem to be consistent if result is kJ/m^2.
        return (150 + 400 * (delta_a ** 0.5)) * 1000

    # Applied Driving Force (J_applied)
    analysis = RCurveAnalysis(resistance_func=material_resistance)

    # Use standard steel E = 200 GPa
    critical_stress = analysis.find_instability_load(
        initial_crack=0.05,
        youngs_modulus=200e9,
        geometry_factor=1.0
    )

    if critical_stress:
        print(f"Critical Stress for Instability: {critical_stress/1e6:.2f} MPa")
        print(f"Critical Crack Extension: {analysis.critical_values['delta_a']*1000:.2f} mm")

        # Plot
        analysis.plot_stability_diagram()
    else:
        print("No instability point found (stable tearing).")

if __name__ == "__main__":
    main()
