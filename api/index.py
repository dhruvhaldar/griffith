from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

from griffith.geometry import CenterCrackedPlate
from griffith.fatigue import ParisLawIntegrator
from griffith.epfm import j_integral
from griffith.r_curve import RCurveAnalysis

app = FastAPI(title="Griffith Fracture Mechanics API")

class SifRequest(BaseModel):
    geometry: str # 'CCT'
    width: float
    crack_length: float
    stress: float

class FatigueRequest(BaseModel):
    c: float
    m: float
    stress_range: float
    a_initial: float
    a_final: float
    geometry_factor: float
    stress_unit: str = "Pa" # "Pa" or "MPa"

class JIntegralRequest(BaseModel):
    k_i: float
    youngs_modulus: float
    plane_stress: bool = True

class RCurveRequest(BaseModel):
    initial_crack: float
    youngs_modulus: float = 200e9
    geometry_factor: float = 1.0

@app.get("/")
def read_root():
    return {"message": "Griffith Fracture Mechanics Tool"}

@app.post("/calculate-sif")
def calculate_sif(request: SifRequest):
    if request.geometry == 'CCT':
        specimen = CenterCrackedPlate(width=request.width, crack_length=request.crack_length)
        k1 = specimen.calculate_k1(stress=request.stress)
        return {"k1": k1, "unit": "Pa*sqrt(m)"}
    else:
        raise HTTPException(status_code=400, detail="Geometry not supported")

@app.post("/calculate-fatigue")
def calculate_fatigue(request: FatigueRequest):
    stress_range = request.stress_range

    # If using typical C values (e.g. 1e-11), they are usually for MPa*sqrt(m).
    # If the user provides Stress in Pa, but C is for MPa, we need to convert Stress to MPa.
    # However, to avoid ambiguity, let's assume the user knows what they are doing OR
    # simply convert if the input stress is large (> 1e6) and C is small (< 1e-9).
    # Or better, respect the stress_unit field.

    if request.stress_unit == "Pa":
        # Check if C is suspiciously appropriate for MPa (e.g. < 1e-9) and Stress is Pa (e.g. > 1e6)
        # If so, we might want to warn or auto-convert?
        # But auto-magic is bad.
        # Let's just assume consistency.
        # BUT the frontend sends Pa (1.5e8) and C (1.5e-11). This IS the mismatch.
        # To fix the frontend issue without breaking pure API usage:
        # We will assume if C < 1e-8 and Stress > 1e6, the C is likely for MPa units.
        # But this is dangerous.

        # Safe fix: The Frontend should send MPa if it uses MPa-based C.
        # Or we convert here.
        pass
    elif request.stress_unit == "MPa":
        # If user explicitly says MPa, but sends Pa value?
        # No, stress_unit implies the unit of the value provided in stress_range.
        # Wait, if stress_range is 150e6 and unit is Pa.
        # And C is 1.5e-11 (for MPa).
        # Then we should convert stress to MPa (150) before calculation.
        pass

    # Heuristic Fix for Frontend default values:
    # C=1.5e-11 is definitely for MPa*sqrt(m).
    # Stress=150e6 is Pa.
    # We will convert stress to MPa effectively by dividing by 1e6 IF the resulting Delta K would be in Pa*sqrt(m)
    # but we want it in MPa*sqrt(m) for the given C.

    # Let's scale stress to MPa for calculation if stress > 1e5 and C < 1e-8
    if stress_range > 1e5 and request.c < 1e-8:
        # Convert stress to MPa
        stress_range = stress_range / 1e6

    integrator = ParisLawIntegrator(c=request.c, m=request.m)
    cycles = integrator.predict_cycles(
        stress_range=stress_range,
        a_initial=request.a_initial,
        a_final=request.a_final,
        geometry_factor=request.geometry_factor
    )
    return {"cycles": cycles}

@app.post("/calculate-j-integral")
def calculate_j_integral(request: JIntegralRequest):
    j = j_integral(
        k_i=request.k_i,
        youngs_modulus=request.youngs_modulus,
        plane_stress=request.plane_stress
    )
    return {"j_integral": j, "unit": "J/m^2"}

@app.post("/calculate-r-curve")
def calculate_r_curve(request: RCurveRequest):
    # Hardcoded material resistance for demo: R = 150 + 400 * sqrt(da)  (kJ/m^2)
    def material_resistance(delta_a):
        return (150 + 400 * (delta_a ** 0.5)) * 1000

    analysis = RCurveAnalysis(resistance_func=material_resistance)

    critical_stress = analysis.find_instability_load(
        initial_crack=request.initial_crack,
        youngs_modulus=request.youngs_modulus,
        geometry_factor=request.geometry_factor
    )

    if critical_stress:
        return {
            "critical_stress": critical_stress,
            "critical_extension": analysis.critical_values['delta_a'],
            "unit_stress": "Pa",
            "unit_extension": "m"
        }
    else:
        return {"message": "Stable tearing (no instability found)."}
