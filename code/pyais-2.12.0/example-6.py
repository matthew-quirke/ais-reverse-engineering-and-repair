import socket
from pyais.encode import encode_dict

# Define AIS message parameters
msg = {
    "type": 18,
    "mmsi": 512001111,
    "speed": 11,               # 1.1 knots = 11 (in tenths)
    "lon": 177.186691,
    "lat": -17.770461,
    "course": 824,             # 82.4° = 824 (in tenths)
    "heading": 511,            # 511 = Not available
    "accuracy": 0,             # GPS position accuracy: 0 = low (<10m), 1 = high (<10m)
    "radio": 0x12345           # Radio status (can be any 19-bit value)
}

# Encode AIS message into NMEA sentences
nmea_sentences = encode_dict(msg)

# UDP target
UDP_IP = "127.0.0.1"
UDP_PORT = 10110

# Create socket and send each NMEA sentence
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for sentence in nmea_sentences:
    sock.sendto(sentence.encode('ascii'), (UDP_IP, UDP_PORT))
    print(f"Sent: {sentence}")

sock.close()

