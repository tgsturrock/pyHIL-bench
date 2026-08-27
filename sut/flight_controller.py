import json
import socket

def run_sut():
    """ System Under Test: Listen to telmetry broadcast from Physics Engine"""

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"[SUT Online] Listening for Telemetry on {UDP_IP}:{UDP_PORT}...\n")

    try:
        while True:

            # Receive JSON byte stream from Physics Engine
            data, _ = sock.recvfrom(1024)

            # Parse info
            packet = json.loads(data.decode("utf-8"))
            seq = packet["header"]["seq"]
            pos = packet["telemetry"]["position"]

            # Place holder for guidance and control..
            print(f"[SUT] Rx Frame #{seq:05d} | Pos: X={pos[0]:.2f}, Pos: Y={pos[1]:.2f}, Pos: Z={pos[2]:.2f}")
    except KeyboardInterrupt:
        print("\n[SUT] Controller Shutting Down...")
    finally:
        sock.close()

if __name__ == "__main__":
    run_sut()



