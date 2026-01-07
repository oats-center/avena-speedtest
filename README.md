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

### Procedures
#### Background
Two lattepanda 2 are used for testing with Iperf3.

#### Installation
1. Flash [Fedora Server 43](https://fedoraproject.org/server/download) via USB network install
2. Install Podman:
```bash
   sudo dnf install -y podman
```
3. Clone the avena-speedtest repository:
```bash
   git clone https://github.com/oats-center/avena-speedtest
   cd avena-speedtest
```
4. Build the container image:
```bash
   podman build -t avena-speedtest .
```

#### Network Roles
**Server:** Device 1 running the iperf3 server
**Client:** Device 2 running the test script to measure connection to Device 1

#### Running Tests

##### On Device 1 (Server)
Start the iperf3 server:
```bash
iperf3 -s -p 5201
```

##### On Device 2 (Client)
Run the test script to connect to Device 1:
```bash
python iperf_automation_udp_and_tcp.py <device-1-ip> -p 5201 -t 8 -i 20 -o highway_test_Linux_udp -u -b 100M
```

**Parameter Guide:**
python iperf_automation_udp_and_tcp.py <ip address> -p <port> -t <test length> -i <test interval> -o <saved folder>
- `<device-1-ip>`: IP address of Device 1 (server)
- `-p <port>`: Port number (default: 5201)
- `-t <test length>`: Duration of test in seconds
- `-i <test interval>`: Interval between periodic reports
- `-o <saved folder>`: Output directory for results
- `-u`: UDP mode (omit for TCP)
- `-b <bandwidth>`: Target bandwidth
  - `-b 100M` = 100 Mbps
  - `-b 1G` = 1 Gbps
  - `-b 500M` = 500 Mbps
  - `-b 10M` = 10 Mbps
