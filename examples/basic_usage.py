"""Basic usage example for ipc_artsnoa SDK."""

from ipc_artsnoa import IPCClient

# Initialize client with API key
client = IPCClient(api_key='YOUR_API_KEY')

# Get your IP information
data = client.get_ip()
print(f'Your IP: {data["ip"]}, Country: {data["country"]}')

# Query specific IP
google_dns = client.get_ip(ip='8.8.8.8')
print(f'\nGoogle DNS IP: {google_dns["ip"]}')
print(f'Country: {google_dns["country"]}')

# Get detailed response object
response = client.get_ip_detailed()
print(f'\nDetailed Info:')
print(f'IP: {response.ip}')
print(f'Country: {response.country}')
print(f'City: {response.city}')
print(f'ISP: {response.isp}')
if response.latitude and response.longitude:
    print(f'Coordinates: ({response.latitude}, {response.longitude})')
