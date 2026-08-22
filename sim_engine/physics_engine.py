from dataclasses import dataclass

@dataclass
class Vector3D:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

# Implementation of HLR-PHY-OUT-001 Vector Generation and HLR-PHY-IN-001 Discrete Time-Step 
class PhysicsEngine:
    def __init__(self, dt: float = 0.02, mass: float = 1.0, g: float = 9.81):
        self.dt = dt
        self.mass = mass
        self.g = g

        # State vectors
        self.position = Vector3D()
        self.velocity = Vector3D()
        self.acceleration = Vector3D()

    def step(self, external_forces: Vector3D = None) -> dict:
        """Executes one simulation step (dt seconds)."""
        if external_forces is None:
            external_forces = Vector3D()

        # 1 Calculate Acceleration ( F = ma -> a = F/m)
        self.acceleration.x = external_forces.x / self.mass
        self.acceleration.y = external_forces.y / self.mass
        self.acceleration.z = (external_forces.z /self.mass) - self.g

        # 2 Calculate Velocity ( v = v + a * dt )
        self.velocity.x += self.acceleration.x * self.dt
        self.velocity.y += self.acceleration.y * self.dt
        self.velocity.z += self.acceleration.z * self.dt

        # 3. Calculate Position
        self.position.x += self.velocity.x * self.dt
        self.position.y += self.velocity.y * self.dt
        self.position.z += self.velocity.z * self.dt


        # Implementation of HLR-PHY-BEH-001 "Ground Plane Constraint"
        # 4 Make sure there is a ground boundary ( z = 0 )
        if self.position.z <= 0.0:
            self.position.z = 0.0
            # If moving below z = 0 put acceleration and velocity to 0
            if self.velocity.z < 0.0:
                self.velocity.z = 0
                self.acceleration.z = max(0.0, self.acceleration.z)

        return {
            "position": [self.position.x, self.position.y, self.position.z],
            "velocity": [self.velocity.x, self.velocity.y, self.velocity.z],
            "acceleration": [self.acceleration.x, self.acceleration.y, self.acceleration.z]
        }

    def get_state(self) -> dict:
        """Returns the current truth kinematic vectors."""
        return {
            "position": self.position,
            "velocity": self.velocity,
            "acceleration": self.acceleration,
    }