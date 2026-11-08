# taran-tula — Cheat Sheet

> Threaded TCP **connect** scanner (stdlib `socket` + `ThreadPoolExecutor`) with optional banner grab.
> Repo: <https://github.com/BBARIBEAU1/taran-tula> · Authorized labs / own hosts only.

## Install / run
```bash
# source: ~/projects/portscanner/taran-tula.py
chmod +x ~/projects/portscanner/taran-tula.py
ln -sf ~/projects/portscanner/taran-tula.py ~/.local/bin/taran-tula   # ~/.local/bin on $PATH
taran-tula -h
```

## Syntax
```text
taran-tula <target> [-p START-END] [-t SECS] [-w THREADS] [-b]
```

| Flag | Long | Default | Meaning |
|---|---|---|---|
| `target` | — | *(required)* | Hostname or IPv4 to scan |
| `-p` | `--ports` | `1-1024` | Port **range** `START-END` (inclusive) |
| `-t` | `--timeout` | `1.0` | Per-connect / recv timeout, seconds (float) |
| `-w` | `--workers` | `100` | Thread count |
| `-b` | `--banners` | off | Grab banner on open ports (passive recv → HTTP `HEAD` fallback → hex if binary) |
| `-h` | `--help` | — | Usage |

## Examples
```bash
taran-tula 127.0.0.1                          # top 1-1024 on localhost
taran-tula 127.0.0.1 -p 1-65535 -w 300        # full range, more threads
taran-tula 127.0.0.1 -p 8000-8000 -b          # single port = START-END
taran-tula 127.0.0.1 -p 20-25 -b -t 2         # slower services, longer wait
taran-tula scanme.nmap.org -p 1-1024 -w 50    # Nmap's permitted practice host (light only)
taran-tula 127.0.0.1 -b | tee scan.txt        # keep results (no -o flag)
```

## Output
```text
Port 22 is OPEN | SSH-2.0-OpenSSH_9.x ...
Port 8000 is OPEN | Server: SimpleHTTP/0.6 Python/3.x
Port 9999 is OPEN | binary data: 0a1b2c...           # first 16 bytes as hex
```

## Workflow
1. Quick sweep `-p 1-1024` → full `-p 1-65535` if needed.
2. Re-run open ports with `-b` to ID services.
3. Hand interesting ports to **shelob** (`shelob <host> -p <port>`) for version → searchsploit.

## Gotchas
- `-p` **must** be `A-B`. `-p 80` or `-p 22,80` crashes (split on `-`). Use `-p 80-80`.
- Only **open** ports print. Closed (RST) and filtered (timeout) are both silent.
- Output order is **not sorted** — threads finish in any order. Pipe through `sort -k2 -n` if needed.
- `-b` is slower: it waits the full `-t` for a passive banner before trying HTTP `HEAD`.
- HTTPS/TLS ports usually show `no banner` or hex — no TLS handshake is done.
- IPv4 only (`AF_INET`). Full connect = logged by the target; it's not stealthy.
- Too many workers on a slow/VPN link → missed ports. Drop `-w` or raise `-t`.
