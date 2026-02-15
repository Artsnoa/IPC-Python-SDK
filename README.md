# IPC Artsnoa Python SDK

Official Python SDK for [ipc.artsnoa.com](https://ipc.artsnoa.com) API - IP geolocation and information service.

## Features

- Simple and intuitive API
- Type hints for better IDE support
- Comprehensive error handling
- Automatic retry logic with exponential backoff
- Environment variable configuration support
- Zero external dependencies (uses standard library only)
- Full test coverage

## Installation

```bash
pip install ipc-artsnoa
```

Or with uv:

```bash
uv add ipc-artsnoa
```

## Quick Start

```python
from ipc_artsnoa import IPCClient

# Initialize client with API key
client = IPCClient(api_key='YOUR_API_KEY')

# Get IP information
data = client.get_ip()
print(f'Your IP: {data["ip"]}, Country: {data["country"]}')
```

## Usage Examples

### Basic Usage

```python
from ipc_artsnoa import IPCClient

# Create client
client = IPCClient(api_key='YOUR_API_KEY')

# Get your own IP info
data = client.get_ip()
print(f"IP: {data['ip']}")
print(f"Country: {data['country']}")
print(f"City: {data['city']}")
```

### Query Specific IP

```python
# Get info for a specific IP
data = client.get_ip(ip='8.8.8.8')
print(f"Google DNS is in {data['country']}")
```

### Detailed Response Object

```python
# Get detailed response object
response = client.get_ip_detailed()
print(f"IP: {response.ip}")
print(f"Country: {response.country}")
print(f"City: {response.city}")
print(f"ISP: {response.isp}")
print(f"Coordinates: ({response.latitude}, {response.longitude})")
```

### Environment Variables

```python
import os
from ipc_artsnoa import IPCClient

# Set API key in environment
os.environ['IPC_API_KEY'] = 'YOUR_API_KEY'

# Create client from environment
client = IPCClient.from_env()
data = client.get_ip()
```

### Custom Configuration

```python
from ipc_artsnoa import IPCClient

# Custom timeout and retry settings
client = IPCClient(
    api_key='YOUR_API_KEY',
    timeout=60,
    max_retries=5,
    user_agent='MyApp/1.0'
)
```

### Location Information

```python
# Get location details
location = client.get_location()
print(f"Location: {location['city']}, {location['country']}")
```

### ISP Information

```python
# Get ISP details
isp = client.get_isp()
print(f"ISP: {isp['isp']}")
```

### Batch Lookup

```python
# Look up multiple IPs at once
ips = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
results = client.batch_lookup(ips)

for ip, data in results.items():
    print(f"{ip}: {data['country']}")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from ipc_artsnoa import (
    IPCClient,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
    NetworkError,
    TimeoutError
)

client = IPCClient(api_key='YOUR_API_KEY')

try:
    data = client.get_ip()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except ValidationError as e:
    print(f"Invalid request: {e}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except TimeoutError as e:
    print(f"Request timeout: {e}")
```

## Environment Variables

The SDK supports the following environment variables:

- `IPC_API_KEY` - Your API key
- `IPC_BASE_URL` - Custom API base URL (default: `https://ipc.artsnoa.com/api`)
- `IPC_TIMEOUT` - Request timeout in seconds (default: `30`)
- `IPC_MAX_RETRIES` - Maximum retry attempts (default: `3`)
- `IPC_VERIFY_SSL` - Verify SSL certificates (default: `true`)

## API Reference

### IPCClient

#### Constructor

```python
IPCClient(
    api_key: str,
    base_url: Optional[str] = None,
    timeout: int = 30,
    max_retries: int = 3,
    verify_ssl: bool = True,
    user_agent: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None
)
```

#### Methods

- `get_ip(ip: Optional[str] = None) -> Dict` - Get IP information
- `get_ip_detailed(ip: Optional[str] = None) -> IPResponse` - Get detailed IP information
- `get_location(ip: Optional[str] = None) -> Dict` - Get location information
- `get_isp(ip: Optional[str] = None) -> Dict` - Get ISP information
- `batch_lookup(ips: List[str]) -> Dict` - Look up multiple IPs

### Class Methods

- `from_env(api_key: Optional[str] = None) -> IPCClient` - Create client from environment variables

## Development

```bash
# Clone repository
git clone https://github.com/artsnoa/ipc-python-sdk.git
cd ipc-python-sdk

# Install dependencies with uv
uv sync

# Run tests
uv run pytest

# Build package
uv build
```

## Requirements

- Python 3.10+
- No external dependencies (uses standard library only)

## License

MIT License

## Support

- Documentation: [https://github.com/artsnoa/ipc-python-sdk](https://github.com/artsnoa/ipc-python-sdk)
- Issues: [https://github.com/artsnoa/ipc-python-sdk/issues](https://github.com/artsnoa/ipc-python-sdk/issues)
- Email: support@artsnoa.com
