#!/usr/bin/env python3

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="taran-tula: threaded TCP port scanner")
parser.add_argument("target", help="Hostname or IP to scan")
parser.add_argument("-p", "--ports", default="1-1024", help="Port range, e.g. 1-1000")
parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout in seconds")
parser.add_argument("-w", "--workers", type=int, default=100, help="Number of threads")
args = parser.parse_args()

start, end = args.ports.split("-")
ports = range(int(start), int(end) + 1)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    result = s.connect_ex((args.target, port))
    s.close()
    if result == 0:
        print(f"Port {port} is OPEN")

print(f"Scanning {args.target} ports {start}-{end}...")
with ThreadPoolExecutor(max_workers=args.workers) as pool:
    pool.map(scan_port, ports)
print("Scan complete.")
