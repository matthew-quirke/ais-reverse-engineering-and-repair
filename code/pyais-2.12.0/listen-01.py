# listen_udp_ais.py
import socket
from pyais.stream import IterMessages

UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on UDP {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(2048)
    lines = data.decode(errors='ignore').splitlines()

    for line in lines:
        print(f"\nRaw NMEA from {addr}: {line.strip()}")

        try:
            for msg in IterMessages.from_string(line):
                decoded = msg.decode()
                print("Decoded AIS message:")
                print(decoded)
        except Exception as e:
            print("Error decoding message:", e)

