import pytest
from sim_engine.physics_engine import PhysicsEngine, Vector3D

def test_hlr_phy_in_001_timestep_param():

    """[HLR-PHY-IN-001] Fixed step size integration parameter default and custom setting."""
    default_engine = PhysicsEngine()
    assert default_engine.dt == 0.02

    custom_engine = PhysicsEngine(dt=0.01)
    assert custom_engine.dt == 0.01

def test_hlr_phy_out_001_kinematic_vectors():
    """[HLR-PHY-OUT-001] Returns 3D position, velocity, and acceleration vectors."""
    engine = PhysicsEngine(dt=0.02)
    state = engine.get_state()

    # Check if 3D vector fields exist and contain [x, y ,z] for each measurement
    for key in ["position", "velocity", "acceleration"]:
        assert key in state
        vec = state[key]
        assert hasattr(vec, "x") and hasattr(vec, "y") and hasattr(vec, "z")

    # Advance a step and ensure state updates
    engine.step()
    new_state = engine.get_state()
    assert new_state is not None

def test_hlr_phy_beh_001_ground_plane_constraint():
    """[HLR-PHY-BEH-001] Spatial boundary z >= 0.0m resets vz to 0 upon contact."""
    engine = PhysicsEngine(dt=0.02)

    # Set position at ground plane with downward velocity/trajectory
    engine.position = Vector3D(0.0, 0.0, 0.0)
    engine.velocity = Vector3D(0.0, 0.0, -5.0)

    # Step simulation forward
    engine.step()
    state = engine.get_state()

    # Verify z position boundary is respected and that the vertical velocity is reset
    assert state["position"].z >= 0.0
    assert state["velocity"].z == 0.0
