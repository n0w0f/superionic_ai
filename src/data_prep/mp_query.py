from constants import MP_API_KEY
from mp_api.client import MPRester
from pymatgen.core import structure


def mp_query_id(composition: str = "ZnO", mp_api_key: str = MP_API_KEY) -> list:
    """Queries structures from Materials Project Database and returns a list of material project ids with different polymorphs
    Args:
        mp_api_key (str): materials project api key
        composition (str): composition of material to be queried

    Returns:
        list of mp-ids (list): Multiple materials project structure ids

    """
    with MPRester(mp_api_key) as mpr:
        mpr = MPRester(mp_api_key)
        mat_id = mpr.get_material_ids(composition)
    print(mat_id)
    return mat_id


def mp_query_structure(mp_id: int = 0, mp_api_key: str = MP_API_KEY) -> structure:
    """Queries mp structures from Materials Project Database and returns pymatgen structure
    Args:
        mp_api_key (str): materials project api key
        mp_id (str): materials project id of the structre
    Returns:
        structure  (structure):  materials project structure
    """
    with MPRester(mp_api_key) as mpr:
        structure = mpr.get_structure_by_material_id(mp_id)
    print(structure)
    return structure
