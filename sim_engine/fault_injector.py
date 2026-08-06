import random
from dataclasses import dataclass
from typing import Optional

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

    def process(self, truth_state: dict) -> Optional[dict]:
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

        # Create copy so to not change original the true data
        corrupted = { 
            "position": list(truth_state["position"]),
            "velocity": list(truth_state["velocity"]),
            "acceleration": list(truth_state["acceleration"]),
        }

        # 2 Inject Gaussian Noise (HRL_FLT-001)
        if self.config.noise_std > 0.0:
            for key in ["position", "velocity", "acceleration"]:
                corrupted[key] = [
                    val + random.gauss(0.0, self.config.noise_std)
                    for val in corrupted[key] # Loop through x, y, z values to inject noise
                ]

        # 3 Inject Constant Bias (HLR-FLT-002)
        if self.config.bias_z != 0.0:
            corrupted["position"][2] += self.config.bias_z

        return corrupted
     
