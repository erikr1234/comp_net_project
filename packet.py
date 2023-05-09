#/usr/bin/python
#Comnetsii APIs for Packet. Rutgers ECE423/544

import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import numpy as np

def create_packet(pkttype, ttl, kval, src, dst, dst1, dst2, dst3, seq, hops, adRoute, LS, CRC, data=None):
    """Create a new packet based on given type"""

    if pkttype == 1:  # HELLO PACKET
        header = struct.pack('BBBL', pkttype, seq, ttl, src)

    elif pkttype == 2:  # HELLO ACK PACKET
        header = struct.pack('BBBLL', pkttype, seq, ttl, src, dst)

    elif pkttype == 3:  # ROUTING PACKET
        header = struct.pack('BBBBBBLLB', pkttype, seq, ttl, pkttype, src, hops, adRoute, LS, CRC)

    elif pkttype == 4:  # UNICAST DATA PACKET
        header = struct.pack('BBBLL', pkttype, seq, ttl, src, dst)
        if data:
            header += bytes(data, 'utf-8')

    elif pkttype == 5:  # MULTICAST DATA PACKET
        # Attach the unicast header to the front of the multicast packet
        unicast_header = struct.pack('BBBLL', 4, seq, ttl, src, dst)
        header = struct.pack('BBBBLLL', pkttype, seq, ttl, kval, dst1, dst2, dst3)
        if data:
            header += bytes(data, 'utf-8')
        header = unicast_header + header

    else:
        raise ValueError("Invalid packet type")

    return header


def read_packet(packet):
    """Read the header and data fields of a packet"""

    # Unpack the type field to determine the packet type
    pkttype = struct.unpack('B', packet[0:1])[0]

    # Parse the header based on the packet type
    if pkttype == 1:  # HELLO PACKET
        header = struct.unpack('BBBL', packet[0:8])
        data = None

    elif pkttype == 2:  # HELLO ACK PACKET
        header = struct.unpack('BBBLL', packet[0:16])
        data = None

    elif pkttype == 3:  # ROUTING PACKET
        header = struct.unpack('BBBBBBLLB', packet[0:16])
        data = None

    elif pkttype == 4:  # UNICAST DATA PACKET
        header = struct.unpack('BBBLL', packet[0:16])
        data = packet[16:].decode('utf-8')

    elif pkttype == 5:  # MULTICAST DATA PACKET
        # Strip off the unicast header before parsing the multicast packet
        unicast_header = struct.unpack('BBBLL', packet[0:16])
        header = struct.unpack('BBBBLLL', packet[16:32])
        data = packet[32:].decode('utf-8')

    else:
        raise ValueError("Invalid packet type")

    return pkttype, header, data
