import warnings
from m3gnet.models import M3GNet, Relaxer
from pymatgen.io.cif import CifParser



for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

model = M3GNet.load()


def run_relax(structure):


    relaxer = Relaxer()  # This loads the default pre-trained model

    relax_results = relaxer.relax(
        structure,    
        fmax = 0.1,
        steps = 500,
        traj_file = None,
        interval=1,
        verbose=False,)

    final_structure = relax_results['final_structure']
    #Energy = float(relax_results['trajectory'].energies[-1]/len(structure))

    return final_structure