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
    

