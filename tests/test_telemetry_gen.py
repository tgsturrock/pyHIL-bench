import json
from sim_engine.physics_engine import Vector3D
from interfaces.telemetry_gen import TelemetryGenerator



def test_hlr_tel_001_json_formatting():
    """[HLR-TEL-001] Verify state dictionary converts to valid JSON string."""
    generator = TelemetryGenerator()

    sample_state = {
        "position": Vector3D(1.12345, 2.67891, 3.0),
        "velocity": Vector3D(0.1, 0.2, 0.3),
        "acceleration": Vector3D(0.0, 0.0, -9.81),
    }

    # 1. Generate payload
    raw_bytes = generator.pack(sample_state, timestamp=100.0)

    assert raw_bytes is not None
    assert isinstance(raw_bytes, bytes)

    # 2. Decode and parse JSON payload
    payload = json.loads(raw_bytes.decode("utf-8"))

    # Assert header metadata
    assert payload["header"]["seq"] == 0
    assert payload["header"]["timestamp"] == 100.0

    # Assert rounded vector values
    assert payload["telemetry"]["position"] == [1.1235, 2.6789, 3.0]
    assert payload["telemetry"]["acceleration"][2] == -9.81

def test_hlr_tel_002_sequence_increment():
    """[HLR-TEL-002] Verify sequence numbers increment per frame and reset cleanly."""
    generator = TelemetryGenerator()

    sample_state = {
        "position": Vector3D(0, 0, 0),
        "velocity": Vector3D(0, 0, 0),
        "acceleration": Vector3D(0, 0, 0),
    }

    # Frame 0
    raw_0 = generator.pack(sample_state)
    assert json.loads(raw_0)["header"]["seq"] == 0

    # Frame 1
    raw_1 = generator.pack(sample_state)
    assert json.loads(raw_1)["header"]["seq"] == 1

    # Reset
    generator.reset_sequence()
    assert generator.sequence_number == 0
    
def test_hlr_tel_003_dropped_packet_handling():
    """[HLR-TEL-003] Verify generator handles None (dropped frame) gracefully."""
    generator = TelemetryGenerator()

    # Pass None (simulating a dropped packet)
    payload = generator.pack(None)

    assert payload is None
    # sim_time should still advance by DT (0.02s)
    assert generator.sim_time == 0.02
