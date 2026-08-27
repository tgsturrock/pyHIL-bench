import sys
import time
from sim_engine.fault_injector import FaultConfig, FaultInjector
from sim_engine.physics_engine import PhysicsEngine
from interfaces.telemetry_gen import TelemetryGenerator
from interfaces.transport import UDPTransport

def run_hil_simulation():
    """ Main Orchestrator exectuting HIL Pilpeline at 50Hz """
    # 1 Engine config and initialitsation
    TARGET_HZ = 50
    LOOP_DT = 1.0 / TARGET_HZ # (20ms loop)
    HOST_IP = "127.0.0.1"
    PORT = 5005

    phys_eng = PhysicsEngine()
    fault_config = FaultConfig(noise_std = 0.05, bias_z = 0.2, packet_drop_prob = 0.2)
    fault_injector = FaultInjector(config = fault_config)
    telemetry = TelemetryGenerator()
    transport = UDPTransport(host = HOST_IP, port = PORT )

    print(f"[HIL BENCH] Starting execution loop @ {TARGET_HZ}Hz (dt={LOOP_DT*1000:.1f}ms)...")
    print(f"[HIL BENCH] Target UDP output: {transport.host}:{transport.port}")
    print("[HIL BENCH] Press Ctrl+C to terminate simulation.\n")

    frame_count = 0
    start_time = time.perf_counter()

    try:
        while True:
            cycle_start = time.perf_counter()

            # Physics engine generates one frame of data
            phys_eng.step()
            truth_state = phys_eng.get_state()

            # Possible fault injection in data
            corrupted_state = fault_injector.inject(truth_state)

            # Send telemetry information
            time_stamp = cycle_start- start_time
            payload = telemetry.pack(corrupted_state, timestamp=time_stamp)
            transport.send(payload)

            # Print out frame telemetry information
            frame_count += 1
            if frame_count % 50 == 0:
                pos = truth_state["position"]
                print(
                    f"[{time_stamp:06.2f}s] Frame: {telemetry.sequence_number:05d} | "
                    f"Pos: X={pos.x:.2f}, Y={pos.y:.2f}, Z={pos.z:.2f}"
                )

            # Make sure every loop/frame cycles at 50Hz (every 20ms)
            elapsed = time.perf_counter()- cycle_start
            sleep_time = LOOP_DT - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n [HIL BENCH] Shuting down simulation")

    finally:
        transport.close()
        print(f"[HIL_BENCH] Closing comms. Total frame count: {frame_count} ")
    
if __name__ == "__main__":
    run_hil_simulation()