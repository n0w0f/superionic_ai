from constants import MP_API_KEY
from pymatgen.ext.matproj import MPRester
from pymatgen.io.cif import CifWriter
import os
from typing import List, Tuple

from utils.read_yaml import read_material_compositions
from utils.manage_files import substitute_element, create_folders_with_names

from data_prep.pymatgen_actions import replace_atom_in_cif_folder
from data_prep.mp_query import mp_query_id

raw_save_path = "/home/nawaf/workflows/superionic_ai/src/data/raw_cifs"
atom_to_replace = "Li"
replacement_atom = "Na"
processed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/processed_cifs"
relaxed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/relaxed_cifs"

def prepare_folders()-> Tuple[List[str], List[str]]:
    # Read material compositions from start_mat.yaml
    materials = read_material_compositions('/home/nawaf/workflows/superionic_ai/src/data/start_mat.yaml')
    print(materials)

    # Substitute element in material compositions
    substituted_materials = substitute_element(materials, atom_to_replace, replacement_atom)
    print(substituted_materials)


    # Create folders for raw CIFs
    create_folders_with_names(materials, raw_save_path)

    # Create folders for processed CIFs
    create_folders_with_names(substituted_materials, processed_save_path)

    # Create folders for relaxed CIFs
    create_folders_with_names(substituted_materials, relaxed_save_path)

    return materials,substituted_materials


def substitute_materials(materials : List[str], substituted_materials : List[str]):
    # Iterate over materials
    for index,material in enumerate(materials):

        # Get material IDs with the same composition
        material_ids = mp_query_id(material)


        # Path where raw CIFs would be stored
        raw_cif_save_path = os.path.join(raw_save_path, material)

        # Query structures using mp-api and save in respective folders
        raw_file_names = query_structures_and_save(material_ids, raw_cif_save_path)
        print(raw_file_names)

        # Path where substituted CIFs would be stored
        processed_cif_save_path = os.path.join(processed_save_path, substituted_materials[index])

        # Substitute all the CIFs in the raw CIF folders with the given atom and store in separate directories
        sub_cif_files = replace_atom_in_cif_folder(raw_cif_save_path, atom_to_replace, replacement_atom, processed_cif_save_path)
        print(sub_cif_files)
    print("Substitution Finished !!! ")

def query_structures_and_save(material_ids: list, save_path: str, mp_api_key: str = MP_API_KEY) ->  List[str]:
    """
    Query the structures of multiple materials using the Materials Project API and store them as CIF files.

    Args:
        material_ids (list): List of Materials Project IDs of the materials.
        api_key (str): Your Materials Project API key.
        save_path (str): Path to save the CIF files.

    Returns:
        None
    """
    file_names: List[str] = []
    with MPRester(mp_api_key) as mpr:
        for material_id in material_ids:
            structure = mpr.get_structure_by_material_id(material_id)

            cif_filename = f"{material_id}.cif"
            cif_path = os.path.join(save_path, cif_filename)

            cif_writer = CifWriter(structure)
            cif_writer.write_file(cif_path)
            file_names.append(cif_path)
    return file_names
