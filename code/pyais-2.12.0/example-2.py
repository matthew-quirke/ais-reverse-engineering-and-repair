# send_ais_udp.py
import socket
import time
from pyais.encode import NMEAMessage
from pyais.messages import MessageType18, MessageType19, MessageType24PartA, MessageType24PartB

UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Common MMSI for this example
MMSI = 244699008

while True:
    # Message 18 - Class B position report
    msg18 = MessageType18(
        mmsi=MMSI,
        speed=5.5,
        lon=172.4567,
        lat=-17.7654,
        course=89.5,
        heading=90
    )
    nmea18 = NMEAMessage.encode(msg18)
    sock.sendto(bytes(nmea18), (UDP_IP, UDP_PORT))

    # Message 19 - Extended position report
    msg19 = MessageType19(
        mmsi=MMSI,
        speed=5.5,
        lon=172.4567,
        lat=-17.7654,
        course=89.5,
        heading=90,
        ship_type=36,
        name="MATYLDA"
    )
    nmea19 = NMEAMessage.encode(msg19)
    sock.sendto(bytes(nmea19), (UDP_IP, UDP_PORT))

    # Message 24 - Static data, part A
    msg24a = MessageType24PartA(mmsi=MMSI, name="MATYLDA")
    nmea24a = NMEAMessage.encode(msg24a)
    sock.sendto(bytes(nmea24a), (UDP_IP, UDP_PORT))

    # Message 24 - Static data, part B
    msg24b = MessageType24PartB(
        mmsi=MMSI,
        ship_type=36,
        vendor_id="RPIAIS",
        callsign="ZMX1234",
        dim_to_bow=5,
        dim_to_stern=7,
        dim_to_port=1,
        dim_to_starboard=1
    )
    nmea24b = NMEAMessage.encode(msg24b)
    sock.sendto(bytes(nmea24b), (UDP_IP, UDP_PORT))

    print("Sent AIS messages 18, 19, 24A, 24B to 127.0.0.1:10110")
    time.sleep(5)
