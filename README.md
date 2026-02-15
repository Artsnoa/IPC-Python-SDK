# IPC Artsnoa Python SDK

Official Python SDK for [ipc.artsnoa.com](https://ipc.artsnoa.com) API - Get your external IP address and location information.

## Features

- Simple and intuitive API
- Type hints for better IDE support
- Comprehensive error handling
- Automatic retry logic with exponential backoff
- Environment variable configuration support
- Zero external dependencies (uses standard library only)

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

# Get your IP information
data = client.get_ip()
print(f'Your IP: {data["ip"]}, Country: {data["country"]}')

# Lookup specific URL
data = client.get_ip(lookup='google.com')
print(f'Google IP: {data["ip"]}')
```

## Usage Examples

### Basic Usage

```python
from ipc_artsnoa import IPCClient

# Create client (API key is optional)
client = IPCClient(api_key='YOUR_API_KEY')

# Get your IP info
data = client.get_ip()
print(f"IP: {data['ip']}")
print(f"Country: {data['country']}")

# Without API key
client = IPCClient()
data = client.get_ip()
print(f"Your IP: {data['ip']}")
```

### URL Lookup

```python
from ipc_artsnoa import IPCClient

# Create client
client = IPCClient(api_key='YOUR_API_KEY')

# Lookup IP for specific URL
data = client.get_ip(lookup='google.com')
print(f"Google IP: {data['ip']}")

data = client.get_ip(lookup='github.com')
print(f"GitHub IP: {data['ip']}")
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

data = client.get_ip()
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from ipc_artsnoa import (
    IPCClient,
    AuthenticationError,
    RateLimitError,
    APIError,
    NetworkError,
    TimeoutError
)

client = IPCClient(api_key='YOUR_API_KEY')

try:
    data = client.get_ip()
    print(f"Your IP: {data['ip']}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
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
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: int = 30,
    max_retries: int = 3,
    verify_ssl: bool = True,
    user_agent: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None
)
```

**Parameters:**
- `api_key` (Optional[str]): API key for authentication. If not provided, some features may be limited.
- `base_url` (Optional[str]): Custom API base URL
- `timeout` (int): Request timeout in seconds
- `max_retries` (int): Maximum retry attempts
- `verify_ssl` (bool): Whether to verify SSL certificates
- `user_agent` (Optional[str]): Custom user agent string
- `headers` (Optional[Dict]): Additional custom headers

#### Methods

##### `get_ip(lookup: Optional[str] = None) -> Dict`

Get IP address and location information.

**Parameters:**
- `lookup` (Optional[str]): URL to lookup IP information for. If not provided, returns your own IP.

**Returns:**
- `Dict`: Dictionary containing IP information with keys: ip, country, etc.

**Example:**
```python
# Get your own IP
data = client.get_ip()

# Lookup specific URL
data = client.get_ip(lookup='google.com')
```

#### Class Methods

##### `from_env(api_key: Optional[str] = None) -> IPCClient`

Create client from environment variables.

**Parameters:**
- `api_key` (Optional[str]): API key override. If not provided, reads from IPC_API_KEY env var.

**Returns:**
- `IPCClient`: Configured client instance

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

- Python 3.10+
- No external dependencies (uses standard library only)

## License

MIT License

## Support

- Documentation: [https://github.com/artsnoa/ipc-python-sdk](https://github.com/artsnoa/ipc-python-sdk)
- Issues: [https://github.com/artsnoa/ipc-python-sdk/issues](https://github.com/artsnoa/ipc-python-sdk/issues)
- Email: support@artsnoa.com
