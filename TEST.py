from scapy.all import ARP, Ether, srp


def scan(ip):
    arp_request = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


ip_range = "192.168.50.0/24"
devices = scan(ip_range)

for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
