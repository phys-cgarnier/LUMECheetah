
from lume.model import LUMEModel
from utils.pv_mapping import get_pv_mad_mapping, accesss_cheetah_attribute, add_noise
import numpy as np
from copy import deepcopy

import torch
from cheetah.accelerator import Segment, Screen
from cheetah.particles import ParticleBeam






class LUMECheetahModel(LUMEModel):
    """Lume Model for Cheetah Simulations"""
    def __init__(self,
                mapping_file,
                simulator, cached_values, supported_variables
                #will delete these later
                #Assume variable instances already created outside and passed in
                #variable_config_file,
):
        super().__init__(simulator, cached_values, supported_variables)
        #These already come from LUMEModel
        self.simulator = simulator
        self.cached_values = {}
        self._supported_variables = supported_variables

        
        self.mapping_file = mapping_file
        #self.variable_config_file = variable_config_file
        self.init_values = {}
        self.mapping = get_pv_mad_mapping(mapping_file)



    def set(self, values: dict[str, float]) -> None:
        """Set control parameters of the Cheetah simulator.

        Args:
            values: Dictionary of variable names and their corresponding values to set.
        """
        # Implement setting logic specific to Cheetah simulator
        for name, value in values.items():
            # Validate and set the value in the simulator
            self.cached_values[name] = value  # Placeholder for actual simulator interaction
        # What should the difference between setting cachd and setting simulator be?
        # Should get just get simulator values?
        #Use mapping to set simulator values. 
        #Simulator can handle energy returns, and shutter? idk.




    def reset(self) -> None:
        self.simulator.reset()
        self.cached_values.clear()  #Clear cached values

    def load_supported_variables(self) -> dict[str, dict]:
        """Load supported variables for the Cheetah simulator."""
        pass
 
    def set_cached_value(self, name: str, value: float) -> None:
        """Set a cached value for a given variable name.

        Args:
            name: The variable name.
            value: The value to cache.
        """
        self.cached_values[name] = value

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
    
    
        

        