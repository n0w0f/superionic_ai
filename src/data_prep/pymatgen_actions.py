import os
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.core.structure import Structure
from typing import List

def replace_atom_in_cif_folder(cif_folder_path: str, atom_to_replace: str, replacement_atom: str, save_path: str) -> List[str]:
    """
    Replace an atom in CIF structures within a folder and save the updated structures as CIF files.

    Args:
        cif_folder_path (str): The path to the folder containing CIF files.
        atom_to_replace (str): The atom to replace.
        replacement_atom (str): The replacement atom.
        save_path (str): The path to save the updated CIF files.

    Returns:
        None
    """
    cif_files = [f for f in os.listdir(cif_folder_path) if f.endswith(".cif")]
    file_names: List[str] = []

    for cif_file in cif_files:
        cif_file_path = os.path.join(cif_folder_path, cif_file)

        cif_parser = CifParser(cif_file_path)
        structure = cif_parser.get_structures(primitive=False)[0]

        indices_to_replace = [i for i, site in enumerate(structure) if site.specie.symbol == atom_to_replace]
        for index in indices_to_replace:
            structure[index] = replacement_atom

        updated_cif_filename = cif_file.replace(".cif", "_updated.cif")
        updated_cif_path = os.path.join(save_path, updated_cif_filename)

        cif_writer = CifWriter(structure)
        cif_writer.write_file(updated_cif_path)
        file_names.append(updated_cif_path)
    return file_names
