#!/usr/bin/env python3

import socket
import time

# AIS NMEA messages to send
ais_sentences = [
    "!AIVDM,1,1,,A,H7`BH2DTCBD4;7>J=5jhio0h7340,0*4C",
    "!AIVDM,1,1,,B,B7`BEW@02k:iRauMCWdkSwsUkP06,0*35",
    "!AIVDM,1,1,,B,H7OflgP58TDj340000000000000,0*68",
    "!AIVDM,1,1,,B,H7OflgTUFC@<96<pnimnm01@8500,0*66",
    "!AIVDM,1,1,,B,B4eHLK000c:hOjMMCQgJ;wS5oP06,0*71",
    "!AIVDM,2,1,1,A,57fu>J`2EiRtGEGGK?Q@PF08D5=@00000000000U2@F665pGN63@C3k3,0*2C",
    "!AIVDM,2,2,1,A,h00000000000000,2*7D",
    "!AIVDM,1,1,,B,B7Oo`s03wk:hBOuMCr;Q0mTQjD`J,0*1C",
    "!AIVDM,1,1,,A,B3M@pMP013:iOdMMBAO:CwWQjDc:,0*4E"
]

# UDP socket settings
UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send each AIS sentence to OpenCPN
for sentence in ais_sentences:
    sock.sendto(sentence.encode('ascii'), (UDP_IP, UDP_PORT))
    print(f"Sent: {sentence}")
    time.sleep(1)  # Small delay so OpenCPN doesn't choke on input

sock.close()

