from sim_engine.fault_injector import FaultConfig, FaultInjector
from sim_engine.physics_engine import Vector3D

def test_hlr_flt_001_gaussian_noise():
    """[HLR-FLT-001] Inject Gaussian noise when noise_std > 0.0."""

    config = FaultConfig(noise_std=1.0)
    injector = FaultInjector(config)

    truth_state = {
        "position": Vector3D(10.0, 10.0, 10.0),
        "velocity": Vector3D(0.0, 0.0, 0.0),
        "acceleration": Vector3D(0.0, 0.0, 0.0)
    }

    # Corrupt data
    corrupted = injector.inject(truth_state)

    assert corrupted is not None
    # Verify values changed after fault injection
    assert corrupted["position"] != [10.0, 10.0, 10.0]

def test_hlr_flt_002_constant_bias_z():
    """[HLR-FLT-002] Apply constant altitude/Z-axis bias to position."""
    config = FaultConfig(bias_z=5.0)
    injector = FaultInjector(config=config)

    truth_state = {
        "position": Vector3D(0.0, 0.0, 10.0),
        "velocity": Vector3D(0.0, 0.0, 0.0),
        "acceleration": Vector3D(0.0, 0.0, 0.0),
    }

    # Corrupt data
    corrupted = injector.inject(truth_state)
    
    assert corrupted is not None
    # Z-axis (index 2) should be 10.0 + 5.0 = 15.0
    assert corrupted["position"].z == 15.0   

     
def test_hlr_flt_003_packet_drop():
    """[HLR-FLT-003] Drop frame (return None) when packet_drop_prob == 1.0."""
    config = FaultConfig(packet_drop_prob=1.0)  # 100% drop probability
    injector = FaultInjector(config=config)

    truth_state = {
        "position": Vector3D(0.0, 0.0, 0.0),
        "velocity": Vector3D(0.0, 0.0, 0.0),
        "acceleration": Vector3D(0.0, 0.0, 0.0),
    }

    corrupted = injector.inject(truth_state)

    # Must return None on dropped packets
    assert corrupted is None
