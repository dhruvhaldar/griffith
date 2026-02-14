from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Griffith Fracture Mechanics Tool"}

def test_calculate_sif():
    response = client.post("/calculate-sif", json={
        "geometry": "CCT",
        "width": 0.1,
        "crack_length": 0.02,
        "stress": 200e6
    })
    assert response.status_code == 200
    data = response.json()
    assert "k1" in data
    # K = sigma * sqrt(pi * a/2 * sec(...))
    # a = 0.01. alpha = 0.2. sec(pi*0.1) = 1.05
    # approx K = 200e6 * sqrt(pi * 0.01) * sqrt(1.05) ~ 35e6 * 1.02 ~ 36 MPa sqrt(m)
    assert data["k1"] > 30e6

def test_calculate_fatigue():
    response = client.post("/calculate-fatigue", json={
        "c": 1.5e-11,
        "m": 3.0,
        "stress_range": 150e6,
        "a_initial": 0.002,
        "a_final": 0.020,
        "geometry_factor": 1.12
    })
    assert response.status_code == 200
    data = response.json()
    assert "cycles" in data
    assert data["cycles"] > 0

def test_calculate_r_curve():
    response = client.post("/calculate-r-curve", json={
        "initial_crack": 0.05,
        "youngs_modulus": 200e9,
        "geometry_factor": 1.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "critical_stress" in data
    assert data["critical_stress"] > 0
