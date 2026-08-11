import json
import time 
from typing import Optional

class TelemetryGenerator:
    """Combines physics ground truth with fault injection modifiers and serializes to JSON."""

    # [HLR_TEL_002] PT.1 Set port to 5005 and transfer rate at 50 Hz
    DEFAULT_PORT = 5005
    TARGET_HZ = 50
    DT = 1.0 / TARGET_HZ  # 0.02s
    
    def __init__(self):
        self.sequence_number = 0
        self.sim_time = 0.0

    def pack(self, state: Optional[dict], timestamp: Optional[float] = None) -> Optional[bytes]:
        """
        Takes raw truth state from the Physics Engine, applies active fault injection,
        and serializes the result into JSON bytes over UDP.

        Args:
            state (dict | None): Corrupted state from fault_injector (or None if dropped).
            timestamp (float | None): Optional explicit simulation timestamp.

        Returns:
            bytes: Encoded payload ready for socket transmission.
            None: If the frame was dropped upstream.
        """

        # If fault injector dropped frame, return empty byte
        if state is None:
            self.sim_time += self.DT
            return None

        # Fallback to system epoch time if no timestamp 
        ts = timestamp if timestamp is not None else time.time()


        # [HLR_TEL_002] Serialize telemetry frames into JSON format
        
        # Format packet into dict for JSON formating
        payload = {
            "header": {
                "seq": self.sequence_number,
                "timestamp": round(ts, 4),
            },
            "telemetry": {
                "position": [round(v, 4) for v in state["position"]],
                "velocity": [round(v, 4) for v in state["velocity"]],
                "acceleration": [round(v, 4) for v in state["acceleration"]],
            },
        }

        # Increment packet sequence count
        self.sequence_number += 1
        self.sim_time += self.DT

        # Encode Python dict to JSON bytes string
        return json.dumps(payload).encode("utf-8")

    def reset_sequence(self):
        "Reset counter for fresh test run"
        self.sequence_number = 0
        self.sim_time = 0.0
