import pytest
import socket
from interfaces.transport import UDPTransport


def test_hlr_trn_001_socket_handling():
    """[HLR-TRN-001] Verify socket initialization, sending payload, and closing."""
    # Use loopback and port 0 to let OS select port
    host = "127.0.0.1"
    port = 0
    buff_size = 1024
    
    # 1 Setup local reciver socket to catch transmitted telemetry
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver.bind((host,port))
    recv_port = receiver.getsockname()[1]
    receiver.settimeout(1.0)

    # 2 Init sender transport target pointing to receiver
    transport = UDPTransport(host=host, port=recv_port)
    test_data = b'{"header": {"seq": 0}, "telemetry": {"position":[0.0.0]}}'

    # 3 Send payload
    success = transport.send(test_data)
    assert success is True

    # 4 Verify receiver gets exact byte string
    received_bytes, addr = receiver.recvfrom(buff_size)
    assert received_bytes == test_data 

    # 5 Clean up
    transport.close()
    receiver.close()

def test_hlr_trn_002_dropped_frame_handling():
    """[HLR-TRN-002] Verify sending None (dropped packet) transmits 0 bytes without error."""
    transport = UDPTransport(host="127.0.0.1", port=5005)

    # When telemetry generator returns None (packet drop), transport should return 0
    bytes_sent = transport.send(None)
    assert bytes_sent == 0

    transport.close()