import torch
from copy import deepcopy
from cheetah.accelerator import Segment, Screen
from cheetah.particles import ParticleBeam




class CheetahSimulator():
    def __init__(self, lattice_file: str,
                subcell_dest: str = None,
                initial_beam_distribution: ParticleBeam = None)-> None:
        
        self.lattice_file = lattice_file
        self.subcell_dest = subcell_dest
        self.initial_beam_distribution = initial_beam_distribution
        self.beam_distribution = initial_beam_distribution
        self.initial_beam_distribution_charge = (
            initial_beam_distribution.particle_charges
        )

        self.setup_lattice()
        self.track()

    #TODO: what does lattice do with particle beam other than track.
    def setup_lattice(self):
        self.lattice = Segment.from_lattice_json(self.lattice_file)
        for ele in self.lattice.elements:
            if isinstance(ele, Screen):
                ele.method = "histogram"
        
        if self.subcell_dest:
            self.lattice = self.lattice.subcell(end=self.subcell_dest)
    

    def reset(self):
        self.setup_lattice()
        self.beam_distribution = self.initial_beam_distribution

    def track(self):
        self.lattice.track(self.beam_distribution)
    

    def get_energy(self):
        """
        Get the energy of the beam in the virtual accelerator simulator at
        every element for use in calculating the magnetic rigidity.

        Note: need to track on a copy of the lattice to not influence readings!
        """
        test_beam = ParticleBeam(
            torch.zeros(1, 7), energy=self.initial_beam_distribution.energy
        )
        test_lattice = deepcopy(self.lattice)
        element_names = [e.name for e in test_lattice.elements]
        return dict(
            zip(
                element_names,
                test_lattice.get_beam_attrs_along_segment(("energy",), test_beam)[0],
            )
        )

    def set_shutter(self, value: bool):
        """
        Set the beam shutter state in the virtual accelerator simulator.
        If `value` is True, the shutter is closed (no beam), otherwise it is open (beam present).
        """
        if value:
            self.initial_beam_distribution.particle_charges = torch.tensor(0.0)
        else:
            self.initial_beam_distribution.particle_charges = (
                self.initial_beam_distribution_charge
            )
    
    