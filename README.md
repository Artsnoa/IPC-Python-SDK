# IPC Artsnoa Python SDK

Official Python SDK for [ipc.artsnoa.com](https://ipc.artsnoa.com) API - Get your IP address and location information.

## Features

- Simple and intuitive API
- Type hints for better IDE support
- Comprehensive error handling
- Context manager support
- Minimal dependencies

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

# Initialize client (API key is optional)
client = IPCClient(api_key='YOUR_API_KEY')

# Get basic IP information
data = client.get_ip()
print(f'Your IP: {data["ip"]}, Country: {data["country"]}')

# Get detailed IP information
details = client.get_ip_details()
print(f'IP: {details["ip"]}, ASN: {details["asn"]}, Currency: {details["currency"]}')
```

## Usage Examples

### Basic Usage

```python
from ipc_artsnoa import IPCClient

# Create client with API key
client = IPCClient(api_key='YOUR_API_KEY')

# Get basic IP information
data = client.get_ip()
print(f"IP: {data['ip']}")
print(f"Country: {data['country']}")

# Without API key
client = IPCClient()
data = client.get_ip()
print(f"Your IP: {data['ip']}")
```

### Detailed IP Information

```python
from ipc_artsnoa import IPCClient

client = IPCClient(api_key='YOUR_API_KEY')

# Get detailed information including ASN, currency, languages
details = client.get_ip_details()
print(f"IP: {details['ip']}")
print(f"User Agent: {details['userAgent']}")
print(f"ASN: {details['asn']}")
print(f"Country: {details['country']}")
print(f"Currency: {details['currency']}")
print(f"Languages: {details['languages']}")
print(f"Timestamp: {details['timestamp']}")
```

### SDK Version Information

```python
from ipc_artsnoa import IPCClient

client = IPCClient()

# Get available SDK versions
versions = client.get_sdk_versions()
print(f"Python SDK: {versions['python']}")
print(f"JavaScript SDK: {versions['javascript']}")
```

### Custom Configuration

```python
from ipc_artsnoa import IPCClient

# Custom timeout
client = IPCClient(
    api_key='YOUR_API_KEY',
    timeout=15.0
)

data = client.get_ip()
```

### Using Context Manager

```python
from ipc_artsnoa import IPCClient

# Automatically closes session when done
with IPCClient(api_key='YOUR_API_KEY') as client:
    data = client.get_ip()
    print(f"IP: {data['ip']}")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from ipc_artsnoa import (
    IPCClient,
    IPCError,
    IPCAPIError,
    IPCConnectionError,
    IPCTimeoutError
)

client = IPCClient(api_key='YOUR_API_KEY')

try:
    data = client.get_ip()
    print(f"Your IP: {data['ip']}")
except IPCAPIError as e:
    print(f"API error: {e}")
    if hasattr(e, 'status_code'):
        print(f"Status code: {e.status_code}")
except IPCConnectionError as e:
    print(f"Connection error: {e}")
except IPCTimeoutError as e:
    print(f"Request timeout: {e}")
except IPCError as e:
    print(f"IPC error: {e}")
```

## API Reference

### IPCClient

#### Constructor

```python
IPCClient(
    api_key: str | None = None,
    timeout: float = 10.0
)
```

**Parameters:**
- `api_key` (str | None): API key for authentication. Optional.
- `timeout` (float): Request timeout in seconds. Defaults to 10.0

#### Methods

##### `get_ip() -> dict`

Get basic IP address and location information.

**Returns:**
- Dictionary containing basic IP information including:
  - `ip`: Your IP address
  - `country`: Country code

**Raises:**
- `IPCAPIError`: When API returns an error response
- `IPCConnectionError`: When connection fails
- `IPCTimeoutError`: When request times out

**Example:**
```python
data = client.get_ip()
print(f"IP: {data['ip']}, Country: {data['country']}")
```

##### `get_ip_details() -> dict`

Get detailed IP address information.

**Returns:**
- Dictionary containing detailed IP information including:
  - `ip`: Your IP address
  - `userAgent`: Browser user agent string
  - `asn`: Autonomous System Number
  - `country`: Country code
  - `currency`: Country currency code
  - `languages`: Supported languages
  - `timestamp`: Request timestamp
  - `version`: API version

**Raises:**
- `IPCAPIError`: When API returns an error response
- `IPCConnectionError`: When connection fails
- `IPCTimeoutError`: When request times out

**Example:**
```python
details = client.get_ip_details()
print(f"IP: {details['ip']}, ASN: {details['asn']}")
```

##### `get_sdk_versions() -> dict`

Get available SDK versions.

**Returns:**
- Dictionary containing SDK versions for different platforms:
  - `python`: Python SDK version
  - `javascript`: JavaScript SDK version

**Raises:**
- `IPCAPIError`: When API returns an error response
- `IPCConnectionError`: When connection fails
- `IPCTimeoutError`: When request times out

**Example:**
```python
versions = client.get_sdk_versions()
print(f"Python SDK: {versions['python']}")
```

##### `close()`

Close the underlying HTTP session.

**Example:**
```python
client.close()
```

#### Context Manager Support

The client supports context manager protocol for automatic resource cleanup:

```python
with IPCClient(api_key='YOUR_API_KEY') as client:
    data = client.get_ip()
```

## Development

```bash
# Clone repository
git clone https://github.com/artsnoa/ipc-python-sdk.git
cd ipc-python-sdk

# Install dependencies with uv
uv sync

# Build package
uv build
```

## Requirements

- Python 3.10 or higher
- requests >= 2.31.0

## License

MIT License

## Support

- Documentation: [https://github.com/artsnoa/ipc-python-sdk](https://github.com/artsnoa/ipc-python-sdk)
- Issues: [https://github.com/artsnoa/ipc-python-sdk/issues](https://github.com/artsnoa/ipc-python-sdk/issues)
- Email: aurora@artsnoa.com
