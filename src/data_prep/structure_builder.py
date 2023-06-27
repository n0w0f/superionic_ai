from constants import MP_API_KEY
from pymatgen.ext.matproj import MPRester
from pymatgen.io.cif import CifWriter
import os

def query_structures_and_save(material_ids: list, save_path: str, mp_api_key: str = MP_API_KEY) -> None:
    """
    Query the structures of multiple materials using the Materials Project API and store them as CIF files.

    Args:
        material_ids (list): List of Materials Project IDs of the materials.
        api_key (str): Your Materials Project API key.
        save_path (str): Path to save the CIF files.

    Returns:
        None
    """
    with MPRester(mp_api_key) as mpr:
        for material_id in material_ids:
            structure = mpr.get_structure_by_material_id(material_id)

            cif_filename = f"{material_id}.cif"
            cif_path = os.path.join(save_path, cif_filename)

            cif_writer = CifWriter(structure)
            cif_writer.write_file(cif_path)
