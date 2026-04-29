import socket
from pyais.encode import encode_dict
import time

# AIS message content — change these as needed
msg = {
    "type": 18,
    "mmsi": 512005521,
    "speed": 10,               # 1.0 knots → 10 (in 0.1 knots)
    "lon": 177.1867,
    "lat": -17.7705,
    "course": 823,             # 82.3° → 823
    "heading": 511,            # Unknown
    "accuracy": 0,
    "radio": 0x12345           # Can be arbitrary
}

# Encode message to NMEA
nmea_sentences = encode_dict(msg)

# Target MarineTraffic AIS input server
# UDP_IP = "5.9.207.224"
# UDP_PORT = 8247 

UDP_IP = "5.9.207.224"
UDP_PORT = 8247

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send each NMEA sentence to MarineTraffic
for sentence in nmea_sentences:
    sock.sendto(sentence.encode('ascii'), (UDP_IP, UDP_PORT))
    print(f"Sent via UDP: {sentence}")

sock.close()
