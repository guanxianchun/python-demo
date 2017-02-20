#-* encoding:utf-8 -*-
'''
Created on 2016��10��7��

@author: martin
'''
import socket,struct,random
import nmap
import socket
import time
import select
import sys
class iphdr(object):

    """
    This represents an IP packet header.
    @assemble packages the packet
    @disassemble disassembles the packet
    """

    def __init__(self, proto=socket.IPPROTO_ICMP, src="0.0.0.0", dst=None):
        self.version = 4
        self.hlen = 5
        self.tos = 0
        self.length = 20
        self.id = random.randint(2 ** 10, 2 ** 16)
        self.frag = 0
        self.ttl = 255
        self.proto = proto
        self.cksum = 0
        self.src = src
        self.saddr = socket.inet_aton(src)
        self.dst = dst or "0.0.0.0"
        self.daddr = socket.inet_aton(self.dst)
        self.data = ""

    def assemble(self):
        header = struct.pack('BBHHHBB',
                             (self.version & 0x0f) << 4 | (self.hlen & 0x0f),
                             self.tos, self.length + len(self.data),
                             socket.htons(self.id), self.frag,
                             self.ttl, self.proto)
        self._raw = header + b"\x00\x00" + self.saddr + self.daddr + self.data
        return self._raw

    @classmethod
    def disassemble(self, data):
        self._raw = data
        ip = iphdr()
        pkt = struct.unpack('!BBHHHBBH', data[:12])
        ip.version = (pkt[0] >> 4 & 0x0f)
        ip.hlen = (pkt[0] & 0x0f)
        ip.tos, ip.length, ip.id, ip.frag, ip.ttl, ip.proto, ip.cksum = pkt[1:]
        ip.saddr = data[12:16]
        ip.daddr = data[16:20]
        ip.src = socket.inet_ntoa(ip.saddr)
        ip.dst = socket.inet_ntoa(ip.daddr)
        return ip

    def __repr__(self):
        return "IP (tos %s, ttl %s, id %s, frag %s, proto %s, length %s) " \
               "%s -> %s" % \
               (self.tos, self.ttl, self.id, self.frag, self.proto,
                self.length, self.src, self.dst)


class udphdr(object):

    def __init__(self, data="", dport=4242, sport=4242):
        self.dport = dport
        self.sport = sport
        self.cksum = 0
        self.length = 0
        self.data = data

    def assemble(self):
        self.length = len(self.data) + 8
        part1 = struct.pack("!HHH", self.sport, self.dport, self.length)
        cksum = self.checksum(self.data)
        cksum = struct.pack("!H", cksum)

        self._raw = part1 + cksum + self.data
        return self._raw

    @classmethod
    def checksum(self, data):
        # XXX implement proper checksum
        cksum = 0
        return cksum

    def disassemble(self, data):
        self._raw = data
        udp = udphdr()
        pkt = struct.unpack("!HHHH", data)
        udp.src_port, udp.dst_port, udp.length, udp.cksum = pkt
        return udp

if __name__ == '__main__':
#     scansock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     scansock.settimeout(5)
# #     print scansock.connect_ex(("172.17.111.167", 161))
#     try:
#         print scansock.sendto('sss',("172.17.111.167", 161))
# #         scansock.recv(10)
#     except socket.timeout:
#         print "Port", 161, "is open."
#     scansock.connect()
#     nm = nmap.PortScanner()
#     nm.scan(hosts='172.17.111.167/24', arguments='-p 161 -sU ')
#     hosts_list = [(x, nm[x][u'udp'][161]['state']) for x in nm.all_hosts()]
#     for host, status in hosts_list:
#         print('{0}:{1}'.format(host, status))


    timeout = 3
    host = "172.17.111.167"
    port = 161
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    udp_header = udphdr(b"00000000000000000", port, 161)
    udp_packet = udp_header.assemble()
    ip_packet_header = iphdr(socket.IPPROTO_UDP, '172.17.23.130', host)
    ip_packet_header.data = udp_packet
    ip_packet = ip_packet_header.assemble()
#     my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    full_packet = ip_packet
    while full_packet:
        sent = my_socket.sendto(full_packet, (host, port))
        full_packet = full_packet[sent:]
    
    ready = select.select([my_socket], [], [], timeout)
    if ready[0] == []:  # Timeout
        print("Timeout")
        sys.exit()
    rec_packet, addr = my_socket.recvfrom(1024)
    print(rec_packet, addr)