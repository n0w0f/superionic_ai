from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core import Structure


from m3gnet.models import MolecularDynamics



'''

from ase.constraints import FixAtoms
elements = [element.symbol for element in structure.composition.elements]
elements.remove('Na')
c1 = FixAtoms(indices=[atom.index for atom in sc_st if atom.symbol == 'P'])
c2 = FixAtoms(indices=[atom.index for atom in sc_st if atom.symbol == 'S'])

sc_st.set_constraint([c1, c2])

sc_st.set_pbc((True, True, True))

'''




def run_md(config: dict, path:str):

    _structure = Structure.from_file(path)
    structure = AseAtomsAdaptor.get_atoms(_structure)
    structure.repeat((2,2,2))
    structure.set_pbc((True, True, True))

    md = MolecularDynamics(
        atoms=structure,
        temperature=config['temperature'],
        ensemble=config['ensemble'],
        timestep=config['timestep'],
        trajectory=config['trajectory'],
        logfile=config['logfile'],
        loginterval=config['loginterval'],
        )
    md.run(steps=config['steps'])



    
from ase.io import Trajectory
from ase.data import atomic_numbers
from ase import units
from ase.md.analysis import DiffusionCoefficient



def calculate_diffusion_coefficient(trajectory: str) -> tuple:
    """
    Calculate the diffusion coefficient from a trajectory file using the pymatgen DiffusionAnalyzer.

    Args:
        trajectory (str): Path to the trajectory file.

    Returns:
        tuple: A tuple containing diffusion coefficients, printed data, and a plot of the diffusion analysis.
    """
    traj = Trajectory(trajectory)
    atoms = traj[0]

    Na_indices = [i for i, atom in enumerate(atoms) if atom.number == atomic_numbers['Na']]

    dc = DiffusionCoefficient( traj =  traj , timestep =  1 * units.fs * 100, atom_indices=Na_indices, molecule=False)
    diffusion_coefficients = dc.get_diffusion_coefficients()
    printed_data = dc.print_data()
    diffusion_plot = dc.plot()

    return diffusion_coefficients
    
    
    
    