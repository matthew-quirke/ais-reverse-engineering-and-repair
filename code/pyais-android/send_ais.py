from pyais.encode import encode_dict
import socket

# Target server and port
HOST = "10.199.180.31"
PORT = 10110

# AIS message data
msg_data = {
    'msg_type': 1,
    'repeat_indicator': 0,
    'mmsi': 123456789,
    'nav_status': 0,
    'rot': 0,
    'sog': 0,
    'position_accuracy': 0,
    'lon': 177.38,
    'lat': -17.68,
    'cog': 0,
    'true_heading': 511,
    'timestamp': 60,
    'special_manoeuvre': 0,
    'spare': 0,
    'raim': 0,
    'radio_status': 0,
}

# Encode to VDM message
vdm = encode_dict(msg_data)
nmea_sentence = str(vdm) + "\r\n"

# Create a UDP socket and send
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(nmea_sentence.encode("ascii"), (HOST, PORT))
    print(f"Sent via UDP: {nmea_sentence.strip()}")


