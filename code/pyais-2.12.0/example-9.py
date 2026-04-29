import socket
from pyais.encode import encode_dict
import time

# Your vessel's MMSI
MMSI = 512005521

# Create AIS Type 18 (Class B Position Report)
msg = {
    "type": 18,
    "mmsi": MMSI,
    "speed": 10,               # 1.0 knots = 10 (tenths of a knot)
    "lon": 177.1867,
    "lat": -17.7705,
    "course": 823,             # 82.3° = 823 (tenths of a degree)
    "heading": 511,            # 511 = not available
    "accuracy": 0,
    "radio": 0x12345           # Can be arbitrary
}

# Encode to !AIVDM message(s)
nmea_sentences = encode_dict(msg)  # Outputs AIVDM sentences by default

# MarineTraffic ingestion server
UDP_IP = "5.9.207.224"
UDP_PORT = 8247

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send each NMEA-encoded sentence
for sentence in nmea_sentences:
    sock.sendto(sentence.encode('ascii'), (UDP_IP, UDP_PORT))
    print(f"Sent AIVDM to MarineTraffic: {sentence}")

sock.close()
