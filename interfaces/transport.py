import socket
from typing import Optional

class UDPTransport: 
    """Handles UDP network delivery to the SUT flight controller."""

    def __init__(self, host: str ="127.0.0.10", port: int = 5005):
        self.host = host
        self.port = port
        self.sock: Optional[socket.socket] = None

    def connect(self)-> None:
        """[HLR-TRN-001] Initializes the non-blocking UDP socket connection."""
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, payload: Optional[bytes])-> bool:
        """Transmits raw telemetry byte payload to the target host/port.
        
        Args:
            payload: Encoded byte stream, or None if packet was dropped by fault injector.
            
        Returns:
            bool: True if sent successfully, False if skipped (None) or failed.
        """

        # HLR-TRN-002: Drop condition handling (skip sending entirely without error)
        if payload is None:
            return False
        # HLR-TRN-001: Lazy-initialize socket on first frame if not already opened
        if self.sock is None:
            self.connect()
        
        try:
            self.sock.sendto(payload, (self.host, self.port))
            return True
        except Exception as err:
            print(f"[UDP Transport Error] Failed to transmit frame: {err}")
            return False

    def close(self)-> None:
        """[HLR-TRN-001] Cleanly closes the socket and releases network resources."""
        if self.sock:
            self.sock.close()
            self.sock = None
    
        