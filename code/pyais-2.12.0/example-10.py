import socket
from pyais.encode import encode_dict

def calculate_checksum(nmea):
    # Compute XOR of all characters between '!' and '*'
    start = nmea.find('!') + 1
    end = nmea.find('*')
    checksum = 0
    for c in nmea[start:end]:
        checksum ^= ord(c)
    return f"{checksum:02X}"

msg = {
    "type": 18,
    "mmsi": 512005521,
    "lon": 177.186691,
    "lat": -17.770461,
    "speed": 1.1,
    "course": 82.4,
}

sentences = encode_dict(msg)

udp_ip = "127.0.0.1"
udp_port = 10110

# udp_ip = "5.9.207.224"
# udp_port = 8247
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for sentence in sentences:
    if sentence.startswith("!AIVDO"):
        # Replace prefix
        sentence = "!AIVDM" + sentence[6:]
        # Remove old checksum
        sentence_without_checksum = sentence.split('*')[0]
        # Recalculate checksum
        checksum = calculate_checksum(sentence_without_checksum + '*')
        # Append new checksum
        sentence = sentence_without_checksum + '*' + checksum

    print(f"Sending sentence: {sentence}")
    sock.sendto(sentence.encode("ascii"), (udp_ip, udp_port))

