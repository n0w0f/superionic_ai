
import os
from typing import List

from models.m3gnet import run_relax
from pymatgen.io.cif import CifWriter

from data_prep.mp_query import mp_query_id
from data_prep.structure_builder import query_structures_and_save
from data_prep.pymatgen_actions import replace_atom_in_cif_folder

from utils.read_yaml import read_material_compositions
from utils.manage_files import substitute_element, create_folders_with_names, read_cif_files


raw_save_path = "/home/nawaf/workflows/superionic_ai/src/data/raw_cifs"


atom_to_replace = "Li"
replacement_atom = "Na"
processed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/processed_cifs"
relaxed_save_path = "/home/nawaf/workflows/superionic_ai/src/data/relaxed_cifs"

def prepare_data():
    materials = read_material_compositions('/home/nawaf/workflows/superionic_ai/src/data/start_mat.yaml')
    print(materials)

    substituted_materials = substitute_element(materials, atom_to_replace, replacement_atom)
    print(substituted_materials) 

    create_folders_with_names(materials, raw_save_path)
    create_folders_with_names(substituted_materials, processed_save_path) 
    create_folders_with_names(substituted_materials, relaxed_save_path)     

    for index in range(len(materials)):


        #given a material composition returns list if mpids of different structures with same composition
        material_ids = mp_query_id(materials[index])

        #path where raw cifs would be stored
        raw_cif_save_path = os.path.join(raw_save_path,materials[index])
        print(raw_cif_save_path)

        # query structures using mp-api and save in respective folders
        query_structures_and_save(material_ids, raw_cif_save_path)
        
        #path where substituted cifs would be stored
        processed_cif_save_path = os.path.join(processed_save_path,substituted_materials[index])
        print(processed_cif_save_path)

        # substitute all the cifs in the raw cif folders with given atom and store in serperate directories
        replace_atom_in_cif_folder(raw_cif_save_path, atom_to_replace, replacement_atom, processed_cif_save_path)



# function to relax the structures
def geometry_optimize(unrelaxed_structure, filename):
    relaxed_struct = run_relax(unrelaxed_structure)
    updated_cif_path = filename.replace(processed_save_path,relaxed_save_path)
    print(updated_cif_path)
    cif_writer = CifWriter(relaxed_struct)
    cif_writer.write_file(updated_cif_path)


    




if __name__ == "__main__":
    
        
    prepare_data()
    structures,filenames = read_cif_files(processed_save_path)
    print(filenames)
    for i in range(len(structures)):
        geometry_optimize(structures[i],filenames[i])




