
from typing import List,Tuple

from models.m3gnet import run_relax, predict_formation_energy,predict_bandgap
from pymatgen.io.cif import CifWriter
from pymatgen.core import Structure


from data_prep.structure_builder import prepare_folders, substitute_materials
from utils.manage_files import  get_all_cif_files


processed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/processed_cifs"
relaxed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/relaxed_cifs"



def workflow()-> Tuple[List[str],List[str]]:

    relaxed_file_names: List[str] = []
    unrelaxed_file_names: List[str] = []
    formation_e: List[float] = []
    bandgaps: List[float] = []

    # Iterate over processed CIFs
    cif_files = get_all_cif_files(processed_save_path)
    for cif_file in cif_files:

        updated_cif_filename = cif_file.replace("_updated.cif","_relaxed.cif") 
        relaxed_cif_filename = updated_cif_filename.replace(processed_save_path,relaxed_save_path)
        
        # Read the unrelaxed structure from the processed CIF
        unrelaxed_structure = Structure.from_file(cif_file)
        unrelaxed_file_names.append(cif_file)

        # Perform geometry optimization (relaxation) on the unrelaxed structure
        relaxed_structure = run_relax(unrelaxed_structure)

        cif_writer = CifWriter(relaxed_structure)
        cif_writer.write_file(relaxed_cif_filename)
        relaxed_file_names.append(relaxed_cif_filename)

        # Perform formation energy prediction on the relaxed structure
        fe = predict_formation_energy(relaxed_structure)
        formation_e.append(fe)
        print(f"calculating formation energy  {fe}")

        # Perform bandgap prediction on the relaxed structure
        bg = predict_bandgap(relaxed_structure)
        bandgaps.append(bg)
        print(f"calculating formation energy  {bg}")
        

    return relaxed_file_names, unrelaxed_file_names,formation_e, bandgaps




if __name__ == "__main__":
        
    #materials,substituted_materials = prepare_folders()

    #sub_cif_files = substitute_materials(materials,substituted_materials)

    relaxed_file_names, unrelaxed_file_names, formation_e_list, bandgap_list =  workflow()
    print(relaxed_file_names)
    print(formation_e_list)

 





