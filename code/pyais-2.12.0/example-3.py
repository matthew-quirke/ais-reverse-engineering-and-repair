from pyais.encode import encode_dict
import socket
import time

# Target UDP address and port
UDP_IP = "127.0.0.1"
UDP_PORT = 10110

# Static ship info
MMSI = 123456000
lat = -17.771015
lon = 177.1859367
sog = 0.5           # Speed over ground in knots
cog = 180.0         # Course over ground in degrees
heading = 180       # True heading in degrees
nav_status = 1      # Anchored
second = 30         # Timestamp in seconds (0-59)

ship_name = "MATYLDA"
ship_type = 79      # Sailing yacht
to_bow = 6
to_stern = 6
to_port = 2
to_starboard = 2
draught = 20        # 2.0 meters in decimeters
callsign = "ZM3244"
destination = "AUSTRALIA"
vendor_ident = "vendor_vendor"

# Send AIS NMEA sentences via UDP
def send_ais_messages(sock, msgs):
    for msg in msgs:
        print("Sending:", msg)
        sock.sendto((msg + '\r\n').encode(), (UDP_IP, UDP_PORT))

# Create UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    while True:
        msg18 = encode_dict({
            'msg_type': 18,
            'repeat': 0,
            'mmsi': MMSI,
            'reserved': 0,
            'speed': sog,
            'accuracy': False,
            'lon': lon,
            'lat': lat,
            'course': cog,
            'heading': heading,
            'second': second,
            'maneuver': 0,
            'radio': 0
        })

        msg19 = encode_dict({
            'msg_type': 19,
            'repeat': 0,
            'mmsi': MMSI,
            'nav_status': nav_status,
            'speed': sog,
            'accuracy': False,
            'lon': lon,
            'lat': lat,
            'course': cog,
            'heading': heading,
            'second': second,
            'ship_type': ship_type,
            'to_bow': to_bow,
            'to_stern': to_stern,
            'to_port': to_port,
            'to_starboard': to_starboard,
            'call_sign': callsign,
            'name': ship_name,
        })

        msg24_part_a = encode_dict({
            'msg_type': 24,
            'repeat': 0,
            'mmsi': MMSI,
            'part_no': 0,
            'name': ship_name
        })

        msg24_part_b = encode_dict({
            'msg_type': 24,
            'repeat': 0,
            'mmsi': MMSI,
            'part_no': 1,
            'ship_type': ship_type,
            'vendor_id': vendor_ident,
            'model': '',
            'serial': '',
            'callsign': callsign,
            'dim_to_bow': to_bow,
            'dim_to_stern': to_stern,
            'dim_to_port': to_port,
            'dim_to_starboard': to_starboard,
            'draught': draught,
            'destination': destination,
        })

        all_msgs = msg18 + msg19 + msg24_part_a + msg24_part_b
        send_ais_messages(sock, all_msgs)
        time.sleep(5)
