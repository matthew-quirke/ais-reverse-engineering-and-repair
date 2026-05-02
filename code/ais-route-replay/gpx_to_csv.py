#!/usr/bin/env python3
import csv
import math
import sys
import xml.etree.ElementTree as ET

DEFAULT_SOG = 6.0  # knots

def bearing_deg(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    y = math.sin(dlon) * math.cos(lat2)
    x = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    )

    return (math.degrees(math.atan2(y, x)) + 360) % 360


if len(sys.argv) < 2:
    print("Usage: python3 gpx_to_csv.py route.gpx [output.csv]")
    sys.exit(1)

gpx_file = sys.argv[1]
csv_file = sys.argv[2] if len(sys.argv) > 2 else "route.csv"

tree = ET.parse(gpx_file)
root = tree.getroot()

ns = {"gpx": "http://www.topografix.com/GPX/1/1"}

points = []

# OpenCPN route points
for pt in root.findall(".//gpx:rtept", ns):
    points.append({
        "lat": float(pt.attrib["lat"]),
        "lon": float(pt.attrib["lon"]),
    })

# Fallback for track GPX files
if not points:
    for pt in root.findall(".//gpx:trkpt", ns):
        points.append({
            "lat": float(pt.attrib["lat"]),
            "lon": float(pt.attrib["lon"]),
        })

if not points:
    raise RuntimeError("No rtept or trkpt points found in GPX file")

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["lat", "lon", "sog", "cog"])

    for i, p in enumerate(points):
        if i < len(points) - 1:
            next_p = points[i + 1]
            cog = bearing_deg(p["lat"], p["lon"], next_p["lat"], next_p["lon"])
        elif len(points) > 1:
            prev_p = points[i - 1]
            cog = bearing_deg(prev_p["lat"], prev_p["lon"], p["lat"], p["lon"])
        else:
            cog = 0.0

        writer.writerow([
            f"{p['lat']:.9f}",
            f"{p['lon']:.9f}",
            f"{DEFAULT_SOG:.1f}",
            f"{cog:.1f}",
        ])

print(f"Wrote {len(points)} points to {csv_file}")
