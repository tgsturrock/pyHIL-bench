import random
from dataclasses import dataclass
from typing import Optional

from sim_engine.physics_engine import Vector3D

@dataclass
class   FaultConfig:
    """Configure active faults to inject into the truth state."""
    noise_std: float = 0.0        # Standard deviation for Gaussian noise
    bias_z: float = 0.0           # Consatant bias on Z-axis (altitude drift)
    packet_drop_prob: float = 0.0 # Probability of dropping a frame (0% (0.0) to 100% (1.0))

class FaultInjector:
    def __init__(self, config: Optional[FaultConfig] = None):
        """If the user passed in a custom config, use it. Otherwise, create a brand-new
           default FaultConfig() object and use that instead"""
        self.config = config if config else FaultConfig()

    def inject(self, truth_state: dict) -> Optional[dict]:
        """
        Receives truth state dictionar, applies configured faults 
        and returns corrupted stats dictionary (or non if packet is dropped)
        """
        # 1. Check for Packet Drop (HLR-FLT-003)
        """Checks if packet drop loss is probable (eg < 0.0) if it is, it rolls the dice for chance of packet loss. 
           Higher packet_drop_prob is (eg closer to 1.0), more chance for packet loss. 
           random.random return num between 0.0 and 1.0 """


        if self.config.packet_drop_prob > 0.0: 
            if random.random() < self.config.packet_drop_prob:
                return None # Sim packet loss

        # Make a fresh Vector3D so modifying corrupted doesn't touch truth_state
        corrupted = {}
        for key, vec in truth_state.items():    
            corrupted[key] = Vector3D(vec.x, vec.y, vec.z)

        # 2 Inject Gaussian Noise (HRL_FLT-001)
        if self.config.noise_std > 0.0:
            for vec in corrupted.values():                
                vec.x += random.gauss(0.0, self.config.noise_std)
                vec.y += random.gauss(0.0, self.config.noise_std)
                vec.z += random.gauss(0.0, self.config.noise_std)

        # 3 Inject Constant Bias (HLR-FLT-002)
        if self.config.bias_z != 0.0:
            corrupted["position"].z += self.config.bias_z

        return corrupted
     
