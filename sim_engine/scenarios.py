import math
from typing import Dict, Any, Protocol
from sim_engine.physics_engine import Vector3D

class FlightScenario(Protocol):
    """Protocol for trajectory scenario generators"""

    duration: float

    def get_forces(self, t: float) -> Vector3D:
        """Returns external forces (Vector3d to apply to sim_engine)"""
        ...

    """Duration control method"""
    def is_complete(self, t: float) -> bool:
        """Returns True if the scenario runtime exceeds its target duration."""
        ...

class TimedScenario:
    """Base class to encapsulate duration logic across scenario implementations."""
    def __init__(self, duration: float = 10.0):
        self.duration = duration

    def is_complete(self, t: float) -> bool:
        return t >= self.duration

class LevelFlight:
    """Constant forward thrust on X axis for steady velocity"""
    def __init__(self, thrust_x: float = 2.0, duration: float = 10.0):
        super().__init__(duration)
        self.thrust_x = thrust_x

    def get_forces(self, t: float) -> Vector3D:
        if self.is_complete(t):
            # Set all forces back to 0 (Hover mode)
            return Vector3D(x=0.0, y=0.0, z=9.81)
        # Counter balance gravity on Z (mass=1.0, g=9.81) and push forward on X
        return Vector3D(x=self.thrust_x, y=0.0, z=9.81)

class VerticalClimb:
    def __init__(self, climb_force: float = 12.0, duration: float = 10.0):
        super().__init__(duration)
        self.climb_force = climb_force

    def get_forces(self, t: float) -> Vector3D:
        if self.is_complete(t):
            # Set all forces back to 0 (Hover mode)
            return Vector3D(x=0.0, y=0.0, z=9.81)
        return Vector3D(x = 0.0, y =0.0, z = self.climb_force)
 
class SpiralClimb:
    def __init__(self, radius_force: float = 3.0, freq: float = 0.5, climb_force: float = 11.0, duration: float = 10.0):
        super().__init__(duration)
        self.radius_force = radius_force
        self.freq = freq
        self.climb_force = climb_force

    def get_forces(self, t: float) -> Vector3D:
        if self.is_complete(t):
            # Set all forces back to 0 (Hover mode)
            return Vector3D(x=0.0, y=0.0, z=9.81)
        
        fx = self.radius_force * math.cos(2 * math.pi * self.freq * t)
        fy = self.radius_force * math.sin(2 * math.pi * self.freq * t)
        return Vector3D(x=fx, y=fy, z=self.climb_force)        