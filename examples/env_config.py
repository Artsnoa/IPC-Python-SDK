"""Environment configuration example for ipc_artsnoa SDK."""

import os
from ipc_artsnoa import IPCClient

# Method 1: Set environment variable and create client
os.environ['IPC_API_KEY'] = 'YOUR_API_KEY'

# Optional: Set additional environment variables
os.environ['IPC_TIMEOUT'] = '60'
os.environ['IPC_MAX_RETRIES'] = '5'

# Create client from environment
client = IPCClient.from_env()

# Use the client
data = client.get_ip()
print(f'IP from env config: {data["ip"]}')

# Method 2: Load API key from .env file (example)
# You would typically use python-dotenv for this:
# from dotenv import load_dotenv
# load_dotenv()
# client = IPCClient.from_env()

# Method 3: Explicit API key with env fallback
api_key = os.getenv('IPC_API_KEY', 'fallback-key')
client = IPCClient(api_key=api_key)

# Custom configuration
client = IPCClient(
    api_key=os.environ['IPC_API_KEY'],
    timeout=60,
    max_retries=5,
    user_agent='MyApp/1.0'
)

print('Client configured successfully')
