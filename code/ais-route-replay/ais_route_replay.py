#!/usr/bin/env python3
import argparse
import csv
import socket
import time
from pyais.encode import encode_dict

MMSI = 512005521
HOST = "5.9.207.224"
PORT = 8247


def read_route(filename):
    points = []

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            points.append({
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "sog": float(row.get("sog", 0.0)),   # knots
                "cog": float(row.get("cog", 0.0)),   # degrees
            })

    if not points:
        raise ValueError("Route file contains no points")

    return points


def send_nmea(sentence):
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        s.sendall((sentence + "\r\n").encode("ascii"))


def make_ais_msg(point):
    now = time.time()

    return {
        "msg_type": 18,
        "repeat": 0,
        "mmsi": MMSI,
        "reserved_1": 0,
        "speed": round(min(point["sog"], 102.2), 1),
        "accuracy": True,
        "lon": point["lon"],
        "lat": point["lat"],
        "course": round(point["cog"] % 360, 1),
        "heading": 511,       # 511 = not available
        "second": int(now) % 60,
        "reserved_2": 0,
        "cs": True,           # Class B CS
        "display": False,
        "dsc": False,
        "band": True,
        "msg22": False,
        "assigned": False,
        "raim": False,
        "radio": 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Send AIS Class B position reports from a CSV route file"
    )

    parser.add_argument(
        "file",
        help="CSV file containing lat, lon, sog, cog"
    )

    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=3.0,
        help="Interval between entries in minutes"
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Loop back to start after final entry"
    )

    args = parser.parse_args()

    route = read_route(args.file)
    sleep_seconds = args.interval * 60

    while True:
        for point in route:
            msg = make_ais_msg(point)
            sentences = encode_dict(msg, talker_id="AIVDM")

            for nmea in sentences:
                print(nmea)
                send_nmea(nmea)

            time.sleep(sleep_seconds)

        if not args.loop:
            break


if __name__ == "__main__":
    main()
