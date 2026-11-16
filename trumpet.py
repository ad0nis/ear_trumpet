#!/usr/bin/env python3
"""trumpet: probe an ear (ear.py) on a range of TCP ports to map which ports
the firewalls between the two systems let through."""
import argparse
import errno
import socket
import sys
import time

# Connection refused: POSIX errno, plus the Winsock code on Windows.
REFUSED_ERRNOS = (errno.ECONNREFUSED, getattr(errno, "WSAECONNREFUSED", 10061))

OPEN = "open"            # the ear answered with the expected pong
OTHER = "other"          # connected, but something other than the ear answered
REFUSED = "refused"      # RST: nothing listening, or a firewall rejecting
TIMEOUT = "timeout"      # no answer: most likely dropped by a firewall
ERROR = "error"          # any other socket error


def parse_ports(spec):
    """Turn '1-1000' or '22,80,443,8000-8100' into a sorted list of ports."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
        else:
            start = end = int(part)
        if not (1 <= start <= end <= 65535):
            raise argparse.ArgumentTypeError("invalid port range: %s" % part)
        ports.update(range(start, end + 1))
    if not ports:
        raise argparse.ArgumentTypeError("no ports given")
    return sorted(ports)


def blow(target, port, timeout):
    """Send 'ping' to target:port and classify what comes back.
    Returns a (status, detail) tuple."""
    try:
        sock = socket.create_connection((target, port), timeout)
    except socket.timeout:
        return TIMEOUT, "no response"
    except (OSError, socket.error) as e:
        if getattr(e, "errno", None) in REFUSED_ERRNOS:
            return REFUSED, "connection refused"
        return ERROR, str(e)

    try:
        sock.sendall(b"ping\n")
        try:
            sock.shutdown(socket.SHUT_WR)
        except (OSError, socket.error):
            pass
        reply = b""
        while True:
            chunk = sock.recv(2048)
            if not chunk:
                break
            reply += chunk
    except socket.timeout:
        if not reply:
            return OTHER, "connected, but no reply"
    except (OSError, socket.error) as e:
        if not reply:
            return OTHER, "connected, then %s" % e
    finally:
        sock.close()

    text = reply.decode("ascii", "replace").strip()
    if not text:
        return OTHER, "connected, but no reply"
    if text == "pong %i" % port:
        return OPEN, text
    if text.startswith("pong "):
        # Reached an ear, but on a different port: port translation in the path.
        return OTHER, "ear answered as '%s' (port translated?)" % text
    return OTHER, "unexpected reply: %r" % text[:60]


def main():
    parser = argparse.ArgumentParser(
        description="Probe an ear (ear.py) on a range of TCP ports to find which "
                    "ports the firewalls in between allow.")
    parser.add_argument("target", help="host name or IP address of the system running ear.py")
    parser.add_argument("-p", "--ports", type=parse_ports, default=parse_ports("1-1000"),
                        help="ports to probe, e.g. 1-1000 or 22,80,443,8000-8100 (default: 1-1000)")
    # Windows retries a refused connection for ~2s before reporting it, so a
    # shorter timeout makes refused ports look like dropped (timeout) ones.
    parser.add_argument("-t", "--timeout", type=float, default=3.0,
                        help="seconds to wait to connect and for a reply (default: 3; "
                             "keep it above 2 on Windows or refused ports show as timeouts)")
    parser.add_argument("-d", "--delay", type=float, default=0.5,
                        help="seconds to wait between ports (default: 0.5)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="only print open ports and the summary")
    args = parser.parse_args()

    results = {}
    print("Probing %s on %i ports..." % (args.target, len(args.ports)))
    try:
        for i, port in enumerate(args.ports):
            if i and args.delay > 0:
                time.sleep(args.delay)
            status, detail = blow(args.target, port, args.timeout)
            results.setdefault(status, []).append(port)
            if not args.quiet or status == OPEN:
                print("%5i  %-8s %s" % (port, status, detail))
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nInterrupted; summary covers the ports probed so far.")

    print("")
    print("Summary for %s:" % args.target)
    for status in (OPEN, OTHER, REFUSED, TIMEOUT, ERROR):
        ports = results.get(status, [])
        print("  %-8s %5i  %s" % (status, len(ports), compress(ports)))


def compress(ports):
    """Turn [1, 2, 3, 5] into '1-3, 5' for compact output."""
    ranges = []
    for port in ports:
        if ranges and port == ranges[-1][1] + 1:
            ranges[-1][1] = port
        else:
            ranges.append([port, port])
    return ", ".join(str(a) if a == b else "%i-%i" % (a, b) for a, b in ranges)


if __name__ == "__main__":
    main()
