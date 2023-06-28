import os
import yaml
from typing import List,Tuple
from dataclasses import dataclass, asdict

from models.m3gnet import run_relax, predict_formation_energy,predict_bandgap
from models.screen import check_conductivity, check_stability
from pymatgen.io.cif import CifWriter
from pymatgen.core import Structure


from data_prep.structure_builder import prepare_folders, substitute_materials
from utils.manage_files import  save_dataclass_list_to_json



# Specify the path to the config.yaml file
config_path = os.path.join("..", "config", "config.yaml")

# Read the config.yaml file
with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)



@dataclass
class material_class:
    relaxed_cif_path: str
    unrelaxed_cif_path: str
    formation_energy: float
    bandgap: float
    stable: bool
    insulator: bool
    diffusion_coefficient: float



def workflow(cif_file : str,  config: dict ) -> material_class:


    updated_cif_filename = cif_file.replace("_updated.cif", "_relaxed.cif")
    relaxed_cif_filename = updated_cif_filename.replace(config['data']['path']['processed_save_path'], config['data']['path']['relaxed_save_path'])

    # Read the unrelaxed structure from the processed CIF
    unrelaxed_structure = Structure.from_file(cif_file)

    # Perform geometry optimization (relaxation) on the unrelaxed structure
    relaxed_structure = run_relax(unrelaxed_structure, config['model']['m3gnet']['relaxer'])

    cif_writer = CifWriter(relaxed_structure)
    cif_writer.write_file(relaxed_cif_filename)

    # Perform formation energy prediction on the relaxed structure
    formation_energy = predict_formation_energy(relaxed_structure, config['model']['m3gnet'])

    stability = check_stability(formation_energy, config['workflow']['screen_cutoffs']['formation_energy'])


    # Perform bandgap prediction on the relaxed structure
    bandgap = predict_bandgap(relaxed_structure, config['model']['m3gnet'])

    insulator = check_conductivity(bandgap, config['workflow']['screen_cutoffs']['bandgap'])

    # Create instances of WorkflowResult data class
    relaxed_result = material_class(relaxed_cif_path=relaxed_cif_filename,
                                    unrelaxed_cif_path=cif_file,
                                    formation_energy=formation_energy,
                                    bandgap=bandgap,
                                    stable=stability,
                                    insulator=insulator,
                                    diffusion_coefficient=0,
                                    )

    return relaxed_result 








if __name__ == "__main__":
        
    materials,substituted_materials = prepare_folders(config_data['data']['path'] , config_data['data']['substitution'] )

    raw_cif_paths , substituted_cif_paths = substitute_materials(materials,substituted_materials,config_data['data']['path'] , config_data['data']['substitution'])

    print(raw_cif_paths)
    print(substituted_cif_paths)


    results: List[material_class] = []
    for cif_file in substituted_cif_paths:

        workflow_result =  workflow(substituted_cif_paths, config_data)
        results.append(workflow_result)

    save_dataclass_list_to_json(results, config_data['data']['path']['results'])



 





