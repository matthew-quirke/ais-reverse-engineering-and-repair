import socket
from pyais.encode import encode_dict

msg = {
    "type": 18,
    "mmsi": 512005521,
    "speed": 10,
    "lon": 177.1867,
    "lat": -17.7705,
    "course": 823,
    "heading": 511,
    "accuracy": 0,
    "radio": 0x12345
}

nmea_sentences = encode_dict(msg)

TCP_IP = "5.9.207.224"
TCP_PORT = 8247

with socket.create_connection((TCP_IP, TCP_PORT)) as sock:
    for sentence in nmea_sentences:
        sock.sendall((sentence + "\r\n").encode('ascii'))
        print(f"Sent via TCP: {sentence}")
