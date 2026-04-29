#!/usr/bin/env python3
import json
import math
import socket
import subprocess
import time
from pyais.encode import encode_dict

MMSI = 512005521
HOST = "10.80.188.9"
PORT = 10110

# Class B CS style:
# <2 kn: normally about 3 minutes
# >2 kn: normally about 30 seconds
SLOW_INTERVAL = 180
FAST_INTERVAL = 30

KNOTS_PER_MPS = 1.943844
EARTH_RADIUS_M = 6371000.0

last_fix = None


def get_location():
    raw = subprocess.check_output(
        ["termux-location", "-p", "gps", "-r", "once"],
        text=True,
        timeout=30,
    )
    return json.loads(raw)


def send_nmea(sentence):
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        s.sendall((sentence + "\r\n").encode("ascii"))


def move_position(lat, lon, cog_deg, speed_kn, dt):
    """Dead-reckon position forward using COG/SOG."""
    speed_mps = speed_kn / KNOTS_PER_MPS
    distance = speed_mps * dt

    brng = math.radians(cog_deg)
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    lat2 = math.asin(
        math.sin(lat1) * math.cos(distance / EARTH_RADIUS_M)
        + math.cos(lat1) * math.sin(distance / EARTH_RADIUS_M) * math.cos(brng)
    )

    lon2 = lon1 + math.atan2(
        math.sin(brng) * math.sin(distance / EARTH_RADIUS_M) * math.cos(lat1),
        math.cos(distance / EARTH_RADIUS_M) - math.sin(lat1) * math.sin(lat2),
    )

    return math.degrees(lat2), math.degrees(lon2)


while True:
    try:
        now = time.time()

        loc = get_location()

        lat = float(loc["latitude"])
        lon = float(loc["longitude"])
        sog = float(loc.get("speed", 0.0)) * KNOTS_PER_MPS
        cog = float(loc.get("bearing", 0.0))

        # If GPS gives no bearing because you're nearly stationary, keep last COG.
        if sog < 0.5 and last_fix:
            cog = last_fix["cog"]

        # Optional smoothing / dynamic movement:
        # If last fix exists, project slightly forward from current GPS time.
        if last_fix:
            dt = max(0, now - last_fix["time"])
            if dt > 0 and sog > 0.2:
                lat, lon = move_position(lat, lon, cog, sog, min(dt, 5))

        msg = {
            "msg_type": 18,
            "repeat": 0,
            "mmsi": MMSI,
            "reserved_1": 0,
            "speed": round(min(sog, 102.2), 1),
            "accuracy": True,
            "lon": lon,
            "lat": lat,
            "course": round(cog % 360, 1),
            "heading": 511,       # 511 = not available
            "second": int(now) % 60,
            "reserved_2": 0,
            "cs": True,           # Class B CS unit
            "display": False,
            "dsc": False,
            "band": True,
            "msg22": False,
            "assigned": False,
            "raim": False,
            "radio": 0,
        }

        # Send as received AIS target, not own-vessel AIVDO
        sentences = encode_dict(msg, talker_id="AIVDM")

        for nmea in sentences:
            print(nmea)
            send_nmea(nmea)

        last_fix = {
            "lat": lat,
            "lon": lon,
            "sog": sog,
            "cog": cog,
            "time": now,
        }

        interval = FAST_INTERVAL if sog >= 2.0 else SLOW_INTERVAL

    except Exception as e:
        print("ERROR:", e)
        interval = 10

    time.sleep(interval)
