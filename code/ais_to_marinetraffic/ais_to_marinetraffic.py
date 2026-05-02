#!/usr/bin/env python3
import json
import socket
import subprocess
import time
from pyais.encode import encode_dict

MMSI = 512009999          # your MMSI only
HOST = "10.80.188.xx"
PORT = 10110              # your MarineTraffic station port
INTERVAL = 1             # seconds

def get_location():
    raw = subprocess.check_output(
        ["termux-location", "-p", "gps", "-r", "once"],
        text=True,
        timeout=30
    )
    return json.loads(raw)

def send_nmea(sentence):
    with socket.create_connection((HOST, PORT), timeout=20) as s:
        s.sendall((sentence + "\r\n").encode("ascii"))

while True:
    try:
        loc = get_location()

        lat = float(loc["latitude"])
        lon = float(loc["longitude"])
        sog = float(loc.get("speed", 0.0)) * 1.94384   # m/s to knots
        cog = float(loc.get("bearing", 0.0))

        msg = {
            "msg_type": 1,
            "mmsi": MMSI,
            "status": 15,      # undefined / default
            "turn": 0,
            "speed": sog,
            "accuracy": 1,
            "lon": lon,
            "lat": lat,
            "course": cog,
            "heading": 511,    # not available
            "second": int(time.time()) % 60,
            "maneuver": 0,
            "raim": False,
            "radio": 0,
        }

        sentences = encode_dict(msg)

        for nmea in sentences:
            print(nmea)
            send_nmea(nmea)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(INTERVAL)
