#!/usr/bin/env python3
"""
Iperf3 automation for network performance testing.
Configured via environment variables for containerized deployment.

Required environment variables:
  SERVER_IP    - iperf3 server IP address
  
Optional environment variables (with defaults):
  PORT         - Server port (default: 5201)
  DURATION     - Test duration in seconds (default: 5)
  INTERVAL     - Interval between tests in seconds (default: 10)
  OUTPUT_DIR   - Output directory (default: /data)
  PROTOCOL     - 'tcp' or 'udp' (default: tcp)
  BANDWIDTH    - UDP bandwidth limit (default: 100M)

Usage:
  podman run --env-file options.env -v ./results:/data:z image_name
"""
import json
import csv
import time
import datetime
import subprocess
import os
from pathlib import Path


def run_tests(server_ip, port, duration, output_dir, test_count, protocol, bandwidth):
    """Run download and upload iperf3 tests."""
    results = {}
    
    # Download test
    print("Running download test...")
    cmd = ['iperf3', '-c', server_ip, '-p', str(port), '-t', str(duration), '-R', '-J']
    if protocol == 'udp':
        cmd.extend(['-u', '-b', bandwidth])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    if protocol == 'udp':
        results['download_mbps'] = data['end']['sum']['bits_per_second'] / 1_000_000
        results['download_jitter_ms'] = data['end']['sum'].get('jitter_ms', 0)
        results['download_lost_packets'] = data['end']['sum'].get('lost_packets', 0)
        results['download_lost_percent'] = data['end']['sum'].get('lost_percent', 0)
    else:
        results['download_mbps'] = data['end']['sum_received']['bits_per_second'] / 1_000_000
    
    # Save raw JSON
    with open(output_dir / f"raw_download_{test_count:03d}.json", 'w') as f:
        f.write(result.stdout)
    
    time.sleep(1)
    
    # Upload test
    print("Running upload test...")
    cmd = ['iperf3', '-c', server_ip, '-p', str(port), '-t', str(duration), '-J']
    if protocol == 'udp':
        cmd.extend(['-u', '-b', bandwidth])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    if protocol == 'udp':
        results['upload_mbps'] = data['end']['sum']['bits_per_second'] / 1_000_000
        results['upload_jitter_ms'] = data['end']['sum'].get('jitter_ms', 0)
        results['upload_lost_packets'] = data['end']['sum'].get('lost_packets', 0)
        results['upload_lost_percent'] = data['end']['sum'].get('lost_percent', 0)
    else:
        results['upload_mbps'] = data['end']['sum_sent']['bits_per_second'] / 1_000_000
    
    # Save raw JSON
    with open(output_dir / f"raw_upload_{test_count:03d}.json", 'w') as f:
        f.write(result.stdout)
    
    return results


def save_to_csv(results, csv_file, test_number, protocol):
    """Save test results to CSV file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Create CSV with headers if it doesn't exist
    if not csv_file.exists():
        with open(csv_file, 'w', newline='') as f:
            if protocol == 'tcp':
                csv.writer(f).writerow(['timestamp', 'test_number', 'download_mbps', 'upload_mbps'])
            else:
                csv.writer(f).writerow([
                    'timestamp', 'test_number', 
                    'download_mbps', 'download_jitter_ms', 'download_lost_packets', 'download_lost_percent',
                    'upload_mbps', 'upload_jitter_ms', 'upload_lost_packets', 'upload_lost_percent'
                ])
    
    # Build row based on protocol
    if protocol == 'tcp':
        row = [timestamp, test_number, results['download_mbps'], results['upload_mbps']]
    else:
        row = [
            timestamp, test_number,
            results['download_mbps'], results['download_jitter_ms'], 
            results['download_lost_packets'], results['download_lost_percent'],
            results['upload_mbps'], results['upload_jitter_ms'],
            results['upload_lost_packets'], results['upload_lost_percent']
        ]
    
    # Append row to CSV
    with open(csv_file, 'a', newline='') as f:
        csv.writer(f).writerow(row)
    
    # Print summary
    if protocol == 'tcp':
        print(f"Test #{test_number}: Down={results['download_mbps']:.2f} Mbps, Up={results['upload_mbps']:.2f} Mbps")
    else:
        print(f"Test #{test_number}: Down={results['download_mbps']:.2f} Mbps, Up={results['upload_mbps']:.2f} Mbps | DL Loss: {results['download_lost_percent']:.2f}%, UL Loss: {results['upload_lost_percent']:.2f}%")


def main():
    # Read configuration from environment variables
    server_ip = os.environ.get('SERVER_IP')
    port = int(os.environ.get('PORT', 5201))
    duration = int(os.environ.get('DURATION', 5))
    interval = int(os.environ.get('INTERVAL', 10))
    output_dir = Path(os.environ.get('OUTPUT_DIR', '/data'))
    protocol = os.environ.get('PROTOCOL', 'tcp').lower()
    bandwidth = os.environ.get('BANDWIDTH', '100M')
    
    # Validate required parameters
    if not server_ip:
        raise ValueError("SERVER_IP environment variable is required")
    
    if protocol not in ['tcp', 'udp']:
        raise ValueError(f"PROTOCOL must be 'tcp' or 'udp', got: {protocol}")
    
    # Setup output
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = output_dir / f"results_{protocol}_{timestamp}.csv"
    
    print(f"Testing {server_ip}:{port} using {protocol.upper()}")
    if protocol == 'udp':
        print(f"UDP bandwidth: {bandwidth}")
    print(f"Results: {csv_file}\n")
    
    # Run continuous tests
    test_count = 0
    while True:
        test_count += 1
        results = run_tests(server_ip, port, duration, output_dir, test_count, protocol, bandwidth)
        save_to_csv(results, csv_file, test_count, protocol)
        time.sleep(interval)


if __name__ == "__main__":
    main()
