# ear_trumpet

ear_trumpet is a tool which consists of an "ear" and a "trumpet". The "ear" is a script which acts as a server which listens on ports 1-1000 with an identical handler. The "trumpet" is a client which attempts to send a message to the ear on ports 1-1000, thereby determining the firewall rules which exist between the two endpoints. This tool is meant to help both redteam and blue team members in evaluating the effectiveness of firewalls encountered in the field. The "ear" exists as a python script, and the "trumpet" exists as both a python script and a powershell script, so both sides can run on any system with a Python 3 interpreter. Both of these may be implemented in other languages if continued use is found for this tool or as other languages become necessary to target other platforms.

## Usage

On the system behind the firewall, start the ear (ports below 1024 need root on Linux/macOS):

```
python3 ear.py
```

On the other system, point the trumpet at it:

```
python3 trumpet.py 192.0.2.10
python3 trumpet.py 192.0.2.10 -p 22,80,443,8000-8100 -t 3 -d 0.5
```

Run `python3 trumpet.py -h` for all options. Each port is reported as one of:

| Result    | Meaning |
|-----------|---------|
| `open`    | The ear answered with the expected `pong <port>`: traffic on that port gets through. |
| `other`   | A connection was made, but something other than the ear answered (a local service, proxy, IPS, or port translation). |
| `refused` | The connection was reset: nothing is listening there, or a firewall is rejecting it. |
| `timeout` | No response: most likely dropped by a firewall. |
| `error`   | Any other socket error (e.g. host unreachable). |


## Acknowledgments

* Credit to [DigiNinja](https://digi.ninja/projects/ear_trumpet.php) for the original ruby "ear trumpet" tool which acted as the inspiration for this tool.
* Credit to [this post](https://stackoverflow.com/questions/35279655/connecting-to-multiple-ports-using-python-socketserver) for most of the "ear.py" code.
* Credit to [jstangroome](https://gist.githubusercontent.com/jstangroome/9adaa87a845e5be906c8/raw/b1ede5ce8aaac41efeeef7959a27d911334e952b/Send-NetworkData.ps1) for the powershell module "Send-NetworkData", which basically acts as netcat, and is the real power behind trumpet.ps1 .

## TODO
- Implement both "trumpet" and "ear" in C# so that both sides be injectable by frameworks like Cobalt Strike and metasploit.
- Add help function to ear.py and trumpet.ps1 (trumpet.py has `-h`).
- Make the ear's port range configurable (trumpet.py has `-p`).
- Achieve feature parity with original ear trumpet project.
