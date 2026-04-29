import socket
import time
from pyais import decode
from pyais.encode import encode_dict

# --- Input AIS NMEA message ---
nmea_input = "!AIVDM,1,1,,A,B7Oi?bP00S:i17uM?qgQ3wn5kP06,0*1C"

# --- Decode and re-encode once (static payload) ---
decoded = decode(nmea_input)
nmea_lines = encode_dict(decoded.asdict())

# --- UDP target ---
UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending AIS message to {UDP_IP}:{UDP_PORT}. Press Ctrl+C to stop.")

try:
    while True:
        for line in nmea_lines:
            print(f"Sent: {line}")
            sock.sendto((line + "\r\n").encode('ascii'), (UDP_IP, UDP_PORT))
        time.sleep(1)  # Send once per second
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    sock.close()

