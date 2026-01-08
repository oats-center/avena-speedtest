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
### Procedures
#### Background
Two devices are used for testing with Iperf3.
#### Installation
1. Flash [Fedora Server 43](https://fedoraproject.org/server/download) via USB network install
2. Install Podman:
```bash
   sudo dnf install -y podman
```
#### Network Roles
**Server:** Device 1 running the iperf3 server
**Client:** Device 2 running the test script to measure connection to Device 1
### Running Tests
#### On Device 1 (Server)
Start the iperf3 server:
```bash
iperf3 -s -p 5201
```
#### On Device 2 (Client)
Pull and run the pre-built container:
**TCP Test:**
```bash
podman run --network host \
  -e SERVER_IP=<device-1-ip> \
  -e PORT=5201 \
  -e DURATION=8 \
  -e OUTPUT_DIR=/results \
  -e TEST_COUNT=1 \
  -e PROTOCOL=tcp \
  -e BANDWIDTH=0 \
  -v ./results:/results \
  ghcr.io/oats-center/avena-speedtest:main
```
**UDP Test:**
```bash
podman run --network host \
  -e SERVER_IP=<device-1-ip> \
  -e PORT=5201 \
  -e DURATION=8 \
  -e OUTPUT_DIR=/results \
  -e TEST_COUNT=1 \
  -e PROTOCOL=udp \
  -e BANDWIDTH=100M \
  -v ./results:/results \
  ghcr.io/oats-center/avena-speedtest:main
```
**Environment Variables:**
- `SERVER_IP`: IP address of Device 1 (server)
- `PORT`: Port number (default: 5201)
- `DURATION`: Test duration in seconds
- `OUTPUT_DIR`: Where to save results inside container
- `TEST_COUNT`: Test iteration number
- `PROTOCOL`: `tcp` or `udp`
- `BANDWIDTH`: Target bandwidth for UDP tests (100M, 1G, 500M, 10M)
