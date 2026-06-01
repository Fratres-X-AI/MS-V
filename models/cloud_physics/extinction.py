"""Beer-Lambert transmittance for obscurant cloud planning.

T = exp(-alpha * CL)
where alpha = mass extinction coefficient (m^2/g)
      CL = concentration-length (g/m^2)

STATUS: Literature-parameter model. Not validated against MS-V fill.
"""

from __future__ import annotations

import math
from typing import Literal

Band = Literal["VIS", "NIR", "MWIR"]


def transmittance(alpha_m2_per_g: float, concentration_length_g_m2: float) -> float:
    """Fraction of radiation transmitted through cloud."""
    if alpha_m2_per_g <= 0 or concentration_length_g_m2 <= 0:
        return 1.0
    return math.exp(-alpha_m2_per_g * concentration_length_g_m2)


def effective_obscuration(
    alpha_m2_per_g: float,
    concentration_length_g_m2: float,
    threshold: float = 0.15,
) -> bool:
    """True if transmittance below threshold (effective screen)."""
    return transmittance(alpha_m2_per_g, concentration_length_g_m2) < threshold
