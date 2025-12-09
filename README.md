# avena-speedtest
Speed test scripts for network benchmarking, with results sent to an avena pipeline

### Iperf3
#### What is it?
Iperf3 is a tool used to measure network performance between two devices.
It allows you to test how much data can be transmitted across a data link.

Iperf3 operates using a client/server model where one device operates as the server and a second device operates as a client.

### Test Types

#### TCP
TCP tests measure reliable throughput, where all packets must be acknowledged (Sent and Received). 
This test shows how much data can be transferred consistently without any error.

#### UDP
UDP tests measure maximum achievable throughput, where Iperf3 tries to push as much data as it can without any reliability gurantees.
This test allows you to observe packet loss, jitter, and latency variation, which is important for time-sensitive applications (eg. operating a robot with live video feed remotely).

### Requirements
#### Software
- A Linux environment such as Fedora Server
- Podman for container deployment
- Git to clone repositories

#### Hardware
- Lattepanda 3 Delta
- Power Source (charger or battery)
- [HaLow Tube](https://store.rokland.com/products/alfa-network-tube-ah-802-11ah-sub-1-ghz-outdoor-ap-cpe-fast-ethernet-poe)
- POE Switch
- GPS Module
- Ethernet Cables

### Procedures
#### Background
Two lattepanda 3 Delta are used for testing with Iperf3.

#### Installation
1. For both Lattepanda 3 Deltas, [Fedora Server 43](https://fedoraproject.org/server/download) was flashed via usb network install.
2. Install Podman if it's not already installed (Check using: podman --version)

#### Network Roles
**Client:** The box (LattePanda) running this container and iperf_automation.py
**Server:** The box (LattePanda) running the iperf3 server (iperf3 -s -p 5201)

### Steps


