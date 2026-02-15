"""Error handling example for ipc_artsnoa SDK."""

from ipc_artsnoa import (
    IPCClient,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
    NetworkError,
    TimeoutError,
)

# Initialize client
client = IPCClient(api_key='YOUR_API_KEY')

# Example 1: Comprehensive error handling
try:
    data = client.get_ip()
    print(f'Success! IP: {data["ip"]}')
except AuthenticationError as e:
    print(f'Authentication failed: {e}')
    print('Please check your API key')
except RateLimitError as e:
    print(f'Rate limit exceeded: {e}')
    print('Please wait before making more requests')
except ValidationError as e:
    print(f'Validation error: {e}')
    print('Check your request parameters')
except TimeoutError as e:
    print(f'Request timeout: {e}')
    print('The request took too long to complete')
except NetworkError as e:
    print(f'Network error: {e}')
    print('Check your internet connection')
except APIError as e:
    print(f'API error: {e}')
    print(f'Status code: {e.status_code}')

# Example 2: Graceful degradation
def get_ip_safe(client):
    """Get IP with fallback."""
    try:
        return client.get_ip()
    except AuthenticationError:
        print('Invalid API key')
        return None
    except RateLimitError:
        print('Rate limited, using cached data')
        return {'ip': 'cached', 'country': 'Unknown'}
    except Exception as e:
        print(f'Unexpected error: {e}')
        return None

result = get_ip_safe(client)
if result:
    print(f'Result: {result}')
