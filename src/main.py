import os
import yaml
from typing import List,Tuple
from dataclasses import dataclass, field

from models.m3gnet import run_relax, predict_formation_energy,predict_bandgap
from models.screen import check_conductivity, check_stability
from models.dynamics import run_md , calculate_diffusion_coefficient
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
    trjaectory_files: List[str] = None
    md_log_files: List[str] = None
    formation_energy: float = 0.0 
    bandgap: float = 0.0
    stable: bool = False
    insulator: bool = False
    diffusion_coefficient: float = 0.0
    fit: bool = False






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

    # Create instances of WorkflowResult data class
    screen_result = material_class(relaxed_cif_path=relaxed_cif_filename,
                                    unrelaxed_cif_path=cif_file,
                                    formation_energy=formation_energy,
                                    stable=stability,
                                    )
    
    #screening  - based on bandgap

    if screen_result.stable:
       
        # Perform bandgap prediction on the relaxed structure
        bandgap = predict_bandgap(relaxed_structure, config['model']['m3gnet'])
        insulator = check_conductivity(bandgap, config['workflow']['screen_cutoffs']['bandgap'])

        # Create instances of WorkflowResult data class
        screen_result.bandgap = bandgap
        screen_result.insulator = insulator

    else:
        print("The material not stable.")
        return screen_result


    #screening  - based on diffusion
    
    if screen_result.insulator and screen_result.stable :
        print("The material fits the criteria.")
        screen_result.fit = True

        
        filename = relaxed_cif_filename.replace( "_relaxed.cif", "md.traj")   
        traj_filename = filename.replace(config['data']['path']['relaxed_save_path'],config['data']['path']['md_traj_save_path'])
        lof_file = traj_filename.replace( "md.traj", 'md.log')

        traj_filename_list : List = []
        lof_file_list : List = []
        diffusion_coefficient_list : List = []


        for temperature in config['workflow']['md_dynamics']['list_of_temp']:

            traj_ = traj_filename.replace('.traj', f'_T{temperature}.traj')
            lof_ = lof_file.replace('.log', f'_T{temperature}.log')
  

            config['workflow']['md_dynamics']['temperature'] = temperature
            config['workflow']['md_dynamics']['trajectory'] = traj_
            config['workflow']['md_dynamics']['logfile'] = lof_
            run_md(config['workflow']['md_dynamics'] , relaxed_cif_filename)


            traj_filename_list.append(traj_)
            lof_file_list.append(lof_)  
            diffusion_coefficient_list.append(calculate_diffusion_coefficient(traj_))
            
        screen_result.diffusion_coefficient = diffusion_coefficient_list
        screen_result.md_log_files = lof_file_list
        screen_result.trjaectory_files = traj_filename_list

        return screen_result 
    
        
       

    else:
        print("The material does not fit the criteria.")
        return screen_result

    



if __name__ == "__main__":
        
    materials,substituted_materials = prepare_folders(config_data['data']['path'] , config_data['data']['substitution'] )

    raw_cif_paths , substituted_cif_paths = substitute_materials(materials,substituted_materials,config_data['data']['path'] , config_data['data']['substitution'])

    print(raw_cif_paths)
    print(substituted_cif_paths)


    results: List[material_class] = []
    for cif_file in substituted_cif_paths:

        workflow_result =  workflow(cif_file, config_data)
        results.append(workflow_result)

    save_dataclass_list_to_json(results, config_data['data']['path']['results'])



 





