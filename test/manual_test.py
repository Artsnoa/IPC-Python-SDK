"""Manual test script for quick verification"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ipc_artsnoa import IPCClient


def test_basic_usage():
    """Test basic usage without API key"""
    print("Test 1: Basic usage without API key")
    client = IPCClient()
    try:
        data = client.get_ip()
        print(f"Success! IP: {data.get('ip')}, Country: {data.get('country')}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def test_with_api_key():
    """Test with API key"""
    print("Test 2: With API key")
    api_key = input("Enter API key (or press Enter to skip): ").strip()
    if api_key:
        client = IPCClient(api_key=api_key)
        try:
            data = client.get_ip()
            print(f"Success! IP: {data.get('ip')}, Country: {data.get('country')}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Skipped")
    print()


def test_custom_url():
    """Test with custom URL"""
    print("Test 3: Custom URL")
    custom_url = "https://ipc.artsnoa.com"  # You can change this
    client = IPCClient(base_url=custom_url)
    try:
        data = client.get_ip()
        print(f"Success! IP: {data.get('ip')}, Country: {data.get('country')}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def test_context_manager():
    """Test using context manager"""
    print("Test 4: Context manager")
    with IPCClient() as client:
        try:
            data = client.get_ip()
            print(f"Success! IP: {data.get('ip')}, Country: {data.get('country')}")
        except Exception as e:
            print(f"Error: {e}")
    print()


def test_timeout():
    """Test with custom timeout"""
    print("Test 5: Custom timeout (0.001s - should fail)")
    client = IPCClient(timeout=0.001)
    try:
        data = client.get_ip()
        print(f"Success! IP: {data.get('ip')}, Country: {data.get('country')}")
    except Exception as e:
        print(f"Expected error: {type(e).__name__}: {e}")
    print()


if __name__ == "__main__":
    print("=== IPC SDK Manual Tests ===\n")
    test_basic_usage()
    test_with_api_key()
    test_custom_url()
    test_context_manager()
    test_timeout()
    print("=== Tests Complete ===")
