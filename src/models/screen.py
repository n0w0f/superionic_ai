from typing import Union


def check_stability(formation_energy: Union[float, int], threshold: Union[float, int]) -> bool:
    """
    Check the stability of a material based on its formation energy and a threshold value.

    Args:
        formation_energy (float or int): The formation energy of the material.
        threshold (float or int): The threshold value for stability.

    Returns:
        bool :
            - True if the formation energy is below or equal to the threshold.
            - False if the formation energy is above the threshold.

    Raises:
        ValueError: If the formation energy or threshold is not a valid number.

    """
    if not isinstance(formation_energy, (float, int)) or not isinstance(threshold, (float, int)):
        raise ValueError("Formation energy and threshold must be valid numbers.")

    if formation_energy <= threshold:
        return True
    else:
        return False


def check_conductivity(bandgap: Union[float, int], threshold: Union[float, int]) -> bool:
    """
    Check the conductivity of a material based on its formation energy and a threshold value.

    Args:
        bandgap (float or int): The bandgap of the material.
        threshold (float or int): The threshold value for conductivity.

    Returns:
        bool :
            - False if the bandgap is below or equal to the threshold.
            - True if the bandgap is above the threshold.

    Raises:
        ValueError: If the bandgap or threshold is not a valid number.

    """
    if not isinstance(bandgap, (float, int)) or not isinstance(threshold, (float, int)):
        raise ValueError("Formation energy and threshold must be valid numbers.")

    if bandgap <= threshold:
        return False
    else:
        return True
