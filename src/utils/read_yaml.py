from typing import List
import yaml

def read_material_compositions(file_path: str) -> List[str]:
    """
    Read a YAML file containing material compositions and return a list of materials.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        List[str]: A list of material compositions.
    """
    with open(file_path, 'r') as file:
        compositions = yaml.safe_load(file)
    return compositions
