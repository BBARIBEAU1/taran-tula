#!/usr/bin/env python3

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

from banner import print_banner

def grab_banner(s):
    try:
        data = s.recv(1024)
        text = data.decode(errors="ignore").strip()
        if text and text.isprintable():
            return text
        return f"binary data: {data[:16].hex()}"
    except socket.timeout:
        try:
            request = f"HEAD / HTTP/1.1\r\nHost: {args.target}\r\n\r\n"
            s.sendall(request.encode())
            response = s.recv(1024).decode(errors="ignore")
            for line in response.splitlines():
                if line.lower().startswith("server:"):
                    return line.strip()
            return response.splitlines()[0] if response else "no banner"
        except (socket.timeout, OSError):
            return "no banner"

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    result = s.connect_ex((args.target, port))
    if result == 0:
        if args.banners:
            print(f"Port {port} is OPEN | {grab_banner(s)}")
        else:
            print(f"Port {port} is OPEN")
    s.close()

def main():
    global args
    parser = argparse.ArgumentParser(description="taran-tula: threaded TCP port scanner")
    parser.add_argument("target", help="Hostname or IP to scan")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range, e.g. 1-1000")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout in seconds")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of threads")
    parser.add_argument("-b", "--banners", action="store_true", help="Grab service banners from open ports")
    parser.add_argument("--no-banner", action="store_true", help="Skip the startup signature banner")
    args = parser.parse_args()

    if not args.no_banner:
        print_banner("taran-tula", "port scanner")

    start, end = args.ports.split("-")
    ports = range(int(start), int(end) + 1)

    print(f"Scanning {args.target} ports {start}-{end}...")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pool.map(scan_port, ports)
    print("Scan complete.")


if __name__ == "__main__":
    main()

