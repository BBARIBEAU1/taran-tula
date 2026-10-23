# Python Threaded Port Scanner

A multi-threaded TCP connect scanner built with Python's standard library (socket, argparse, concurrent.futures).

## Usage
    python3 scanner.py <target> [-p 1-1024] [-t 1.0] [-w 100]

## Example
    python3 scanner.py scanme.nmap.org -p 1-10000 -w 200

## What I learned
- How a TCP connect scan works (3-way handshake, connect_ex return codes)
- Closed vs filtered ports (RST vs timeout)
- Threading for I/O-bound work: 1,024 ports in ~3.4s vs up to ~17 min sequentially
- Building CLI tools with argparse

## Legal
Only scan systems you own or are explicitly authorized to test. scanme.nmap.org permits light scanning by the Nmap project.
