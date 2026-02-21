
import pytest
import numpy as np
import matplotlib.pyplot # Ensure it is loaded for patching
from unittest.mock import MagicMock, patch
from griffith.r_curve import RCurveAnalysis

@patch('matplotlib.pyplot')
def test_plot_stability_diagram_vectorization(mock_plt):
    # Verify that plot_stability_diagram uses vectorized calls

    def resistance_func(delta_a):
        # This function should be called with an array
        if isinstance(delta_a, np.ndarray):
            return (150 + 400 * (delta_a ** 0.5)) * 1000
        else:
            # If called with scalar, it works too, but we want to verify array call
            return (150 + 400 * (delta_a ** 0.5)) * 1000

    mock_r_func = MagicMock(side_effect=resistance_func)

    analysis = RCurveAnalysis(resistance_func=mock_r_func)

    # Manually set critical values to avoid running find_instability_load
    analysis.critical_values = {
        'delta_a': 0.05,
        'a_crit': 0.1,
        'r_crit': 1000,
        'sigma_c': 200e6,
        'initial_crack': 0.05,
        'youngs_modulus': 200e9,
        'geometry_factor': 1.0
    }

    analysis.plot_stability_diagram()

    # Verify resistance_func was called with an array
    # Since we use vectorization now, it should be called once with an array of shape (100,)
    assert mock_r_func.call_count == 1
    call_args = mock_r_func.call_args[0][0]
    assert isinstance(call_args, np.ndarray)
    assert len(call_args) == 100
