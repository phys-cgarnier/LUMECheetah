
from lume.model import LUMEModel
import pydantic





class LUMECheetahModel(LUMEModel):
    """Lume Model for Cheetah Simulations"""
    def __init__(self, lattice_file, beam_file, mapping_file, variable_config_file):
        super().__init__()
        self.lattice_file = lattice_file
        self.beam_file = beam_file
        self.mapping_file = mapping_file
        self.variable_config_file = variable_config_file
        self.cached_values = {}
        self._supported_variables = self.load_supported_variables()



    def set(self, values: dict[str, pydantic.Json]) -> None:
        """Set control parameters of the Cheetah simulator.

        Args:
            values: Dictionary of variable names and their corresponding values to set.
        """
        # Implement setting logic specific to Cheetah simulator
        for name, value in values.items():
            # Validate and set the value in the simulator
            self.cached_values[name] = value  # Placeholder for actual simulator interaction

    def reset(self) -> None:
        """Reset the Cheetah simulator to its initial state."""
        # Implement reset logic specific to Cheetah simulator
        self.cached_values.clear()  # Placeholder for actual simulator reset logic

    def load_supported_variables(self) -> dict[str, pydantic.Json]:
        """Load supported variables for the Cheetah simulator."""
        pass
 
    def set_cached_value(self, name: str, value: pydantic.Json) -> None:
        """Set a cached value for a given variable name.

        Args:
            name: The variable name.
            value: The value to cache.
        """
        self.cached_values[name] = value
        

        