import warnings
from m3gnet.models import M3GNet, Relaxer
from pymatgen.io.cif import CifParser
from pymatgen.core import Structure



for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

model = M3GNet.load()


def predict_formation_energy(pymatgen_struct : Structure, config : dict)-> float:

    m3gnet_e_form = M3GNet.from_dir(config['checkpoints']['formation_energy_checkpoint'])
    e_form_predict = m3gnet_e_form.predict_structure(pymatgen_struct)
    return e_form_predict.numpy().tolist()[0].pop()

def predict_bandgap(pymatgen_struct : Structure, config : dict)-> float:

    m3gnet_bgap = M3GNet.from_dir(config['checkpoints']['bandgap_checkpoint'])
    bgap_predict = m3gnet_bgap.predict_structure(pymatgen_struct)
    return bgap_predict.numpy().tolist()[0].pop()




def run_relax(structure):
    relaxer = Relaxer()  # This loads the default pre-trained model

    relax_results = relaxer.relax(
        structure,    
        fmax = 0.1,
        steps = 500,
        traj_file = None,
        interval=1,
        verbose=True,)

    final_structure = relax_results['final_structure']
    #Energy = float(relax_results['trajectory'].energies[-1]/len(structure))

    return final_structure