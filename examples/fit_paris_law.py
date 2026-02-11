import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

def main():
    """
    Fits Paris Law Parameters (C, m) to experimental data.
    """
    # Simulated Experimental Data (da/dN vs Delta K)
    # Log-Log linear relationship: log(da/dN) = log(C) + m * log(Delta K)

    # True parameters
    C_true = 1.5e-11
    m_true = 3.0

    # Generate synthetic data with noise
    delta_k = np.linspace(10e6, 50e6, 20) # 10 to 50 MPa sqrt(m)
    da_dn_true = C_true * (delta_k ** m_true)

    # Add random noise (log-normal)
    noise = np.random.normal(0, 0.1, len(delta_k)) # 10% scatter in log scale
    da_dn_measured = da_dn_true * np.exp(noise)

    # Perform Regression
    x = np.log(delta_k)
    y = np.log(da_dn_measured)

    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    m_fit = slope
    c_fit = np.exp(intercept)

    print(f"True Parameters: C={C_true:.2e}, m={m_true:.2f}")
    print(f"Fitted Parameters: C={c_fit:.2e}, m={m_fit:.2f}")
    print(f"R-squared: {r_value**2:.4f}")

    # Plot
    plt.figure(figsize=(8, 6))
    plt.loglog(delta_k, da_dn_measured, 'o', label='Experimental Data')
    plt.loglog(delta_k, c_fit * delta_k**m_fit, '-', label=f'Paris Law Fit (m={m_fit:.2f})')
    plt.xlabel(r'Stress Intensity Range $\Delta K$ (Pa$\sqrt{m}$)')
    plt.ylabel(r'Crack Growth Rate $da/dN$ (m/cycle)')
    plt.title('Fatigue Crack Growth Rate')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()

if __name__ == "__main__":
    main()
