# ear_trumpet

ear_trumpet is a tool which consists of an "ear" and a "trumpet". The "ear" is a script which acts as a server which listens on ports 1-1000 with an identical handler. The "trumpet" is a client which attempts to send a message to the ear on ports 1-1000, thereby determining the firewall rules which exist between the two endpoints. This tool is meant to help both redteam and blue team members in evaluating the effectiveness of firewalls encountered in the field. The "ear" currently exists as a python script, and the "trumpet" currently exists as a powershell script. Both of these may be implemented in other languages if continued use is found for this tool or as other languages become necessary to target other platforms.


## Acknowledgments

* Credit to [DigiNinja](https://digi.ninja/projects/ear_trumpet.php) for the original ruby "ear trumpet" tool which acted as the inspiration for this tool.
* Credit to [this post](https://stackoverflow.com/questions/35279655/connecting-to-multiple-ports-using-python-socketserver) for most of the "ear.py" code.
* Credit to [jstangroome](https://gist.githubusercontent.com/jstangroome/9adaa87a845e5be906c8/raw/b1ede5ce8aaac41efeeef7959a27d911334e952b/Send-NetworkData.ps1) for the powershell module "Send-NetworkData", which basically acts as netcat, and is the real power behind trumpet.ps1 .

## TODO
- Implement both "trumpet" and "ear" in C# so that both sides be injectable by frameworks like Cobalt Strike and metasploit.
- Add help function to both scripts.
- Make client and server port ranges configurable.
- Achieve feature parity with original ear trumpet project.
