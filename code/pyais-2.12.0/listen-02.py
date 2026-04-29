#!/usr/bin/env python3


import socket
from pyais import decode

UDP_IP = "10.199.180.31"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for AIS UDP packets on {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # Buffer size 1024 bytes
    try:
        nmea = data.decode('ascii').strip()
        message = decode(nmea)
        print(f"Received from {addr}:")
        print(f"  Msg Type: {message.msg_type}")
        print(f"  MMSI: {message.mmsi}")
        print(f"  Lat, Lon: {getattr(message, 'lat', 'N/A')}, {getattr(message, 'lon', 'N/A')}")
        print(f"  Speed: {getattr(message, 'speed', 'N/A')} knots")
        print(f"  Course: {getattr(message, 'course', 'N/A')}°")
    except Exception as e:
        print("Failed to decode AIS message:", e)
