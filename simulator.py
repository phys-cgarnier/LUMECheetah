import torch
from cheetah.accelerator import Segment, Screen
from cheetah.particles import ParticleBeam




class CheetahSimulator():
    def __init__(self, lattice_file: str,
                subcell_dest: str = None,
                initial_particle_distribution: ParticleBeam = None)-> None:
        
        self.lattice_file = lattice_file
        self.subcell_dest = subcell_dest
        self.initial_beam_distribution = initial_particle_distribution
        self.beam_distribution = initial_particle_distribution
        self.lattice = Segment.from_lattice_json(self.lattice_file)
        if self.subcell_dest:
            self.lattice = self.lattice.subcell(end=self.subcell_dest)

    #TODO: what does lattice do with particle beam other than track.
    def reset(self):
        pass

    def track(self):
        pass

    