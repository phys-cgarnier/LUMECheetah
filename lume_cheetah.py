
from lume.model import LUMEModel
from utils.pv_mapping import get_pv_mad_mapping, access_cheetah_attribute
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
        super().__init__(
            simulator=simulator,
            supported_variables=supported_variables,
        )

        self.simulator = simulator
        self.cached_values = cached_values
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
        self.set_pvs(values)

    def set_pvs(self, values: dict):
        """
        Set the corresponding process variable (PV) to the given value on the virtual accelerator simulator.
        """
        for pv_name, value in values.items():
            # handle the beam shutter separately
            if pv_name == self.simulator.beam_shutter_pv:
                self.set_shutter(value)
                continue

            if pv_name == "VIRT:BEAM:RESET_SIM":
                self.reset()
                continue

            # get the base pv name
            base_pv_name = ":".join(pv_name.split(":")[:3])
            attribute_name = ":".join(pv_name.split(":")[3:])

            # get the beam energy along the lattice -- returns a dict of element names to energies
            beam_energy_along_lattice = self.simulator.beam_energy_along_lattice

            # check if the pv_name is a control variable
            if base_pv_name in self.mapping:
                # set the value in the virtual accelerator simulator
                element = getattr(self.simulator.lattice, self.mapping[base_pv_name].lower())

                # get the beam energy for the element
                energy = beam_energy_along_lattice[self.mapping[base_pv_name].lower()]

                # if there are duplicate elements, just grab the first one (both will be adjusted)
                if isinstance(element, list):
                    element = element[0]

                try:
                    print(
                        "accessing element "
                        + element.name
                        + " to set PV "
                        + pv_name
                        + " to "
                        + str(value)
                    )
                    access_cheetah_attribute(element, attribute_name, energy, value)
                except ValueError as e:
                    raise ValueError(f"Failed to set PV {pv_name}: {str(e)}") from e

            else:
                raise ValueError(f"Invalid PV base name: {base_pv_name}")

        # at the end of setting all PVs, run the simulation with the initial beam distribution
        # this will update all readings (screens, BPMs, etc.) in the lattice
        self.simulator.lattice.track(incoming=self.simulator.beam_distribution)



    def reset(self) -> None:
        self.simulator.reset()
        self.cached_values.clear()  #Clear cached values

 
    def set_cached_value(self, name: str, value: float) -> None:
        """Set a cached value for a given variable name.

        Args:
            name: The variable name.
            value: The value to cache.
        """
        self.cached_values[name] = value

        

        