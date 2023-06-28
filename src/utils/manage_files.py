from typing import List, Tuple
import os
from pymatgen.core import Structure


import json
from dataclasses import asdict


def save_dataclass_list_to_json(data_list, save_path):
    """
    Save a list of data class objects to a JSON file.

    Args:
        data_list (List): List of data class objects.
        save_path (str): Path to save the JSON file.
    """
    json_data = [asdict(data) for data in data_list]

    with open(save_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)



def get_all_cif_files(parent_directory):
    """
    Recursively get all CIF files inside subdirectories within a parent directory.
    Args:
        parent_directory (str): The parent directory to search for CIF files.
    Returns:
        list: A list of file paths to CIF files.
    """
    cif_files = []
    
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file.endswith(".cif"):
                file_path = os.path.join(root, file)
                cif_files.append(file_path)

    return cif_files


def create_folders_with_names(elements: List[str], root_path: str):
    """
    Create folders with names corresponding to the elements in the given list at the specified root path.

    Args:
        elements (List[str]): The list of elements.
        root_path (str): The root path where folders will be created.

    Returns:
        None
    """
    for element in elements:
        folder_path = os.path.join(root_path, element)
        os.makedirs(folder_path, exist_ok=True)


def substitute_element(elements: List[str], substitute_from: str, substitute_to: str) -> List[str]:
    """
    Substitute a substring in all elements of a list with a replacement substring.

    Args:
        elements (List[str]): The list of elements.
        substitute_from (str): The substring to be replaced.
        substitute_to (str): The replacement substring.

    Returns:
        List[str]: The list of elements with the substitution applied.
    """
    substituted_elements = [element.replace(substitute_from, substitute_to) for element in elements]
    return substituted_elements


def read_cif_files(root_directory: str) -> Tuple[List[Structure], List[str]]:
    """
    Read all CIF files in the directories and subdirectories of the given root directory
    and create a list of structures along with their corresponding file names.

    Args:
        root_directory: The root directory containing the CIF files.

    Returns:
        A tuple containing a list of pymatgen Structure objects and a list of corresponding file names.
    """
    structure_list: List[Structure] = []
    file_names: List[str] = []

    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith(".cif"):
                cif_file_path = os.path.join(dirpath, filename)
                try:
                    structure = Structure.from_file(cif_file_path)
                    structure_list.append(structure)
                    file_names.append(cif_file_path)
                except Exception as e:
                    print(f"Error reading CIF file {cif_file_path}: {str(e)}")

    return structure_list, cif_file_path
