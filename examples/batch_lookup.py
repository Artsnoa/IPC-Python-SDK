"""Batch lookup example for ipc_artsnoa SDK."""

from ipc_artsnoa import IPCClient

# Initialize client
client = IPCClient(api_key='YOUR_API_KEY')

# List of IPs to look up
ips_to_check = [
    '8.8.8.8',       # Google DNS
    '1.1.1.1',       # Cloudflare DNS
    '208.67.222.222', # OpenDNS
]

# Batch lookup
print('Looking up multiple IPs...\n')
results = client.batch_lookup(ips_to_check)

# Process results
for ip, data in results.items():
    print(f'IP: {ip}')
    print(f'  Country: {data.get("country", "Unknown")}')
    print(f'  ISP: {data.get("isp", "Unknown")}')
    print()

# Example: Filter results by country
us_ips = [ip for ip, data in results.items() if data.get('country') == 'US']
print(f'IPs in the US: {us_ips}')
