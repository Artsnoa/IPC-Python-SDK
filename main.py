"""Simple demo of ipc_artsnoa SDK."""

from ipc_artsnoa import IPCClient


def main():
    """Run a simple demo of the SDK."""
    print("IPC Artsnoa Python SDK Demo")
    print("=" * 50)

    # Note: Replace 'YOUR_API_KEY' with your actual API key
    # or set IPC_API_KEY environment variable
    api_key = 'YOUR_API_KEY'

    try:
        # Initialize client
        client = IPCClient(api_key=api_key)

        # Get IP information
        print("\nFetching your IP information...")
        data = client.get_ip()

        print(f"\nResults:")
        print(f"  IP Address: {data['ip']}")
        print(f"  Country: {data.get('country', 'N/A')}")
        print(f"  City: {data.get('city', 'N/A')}")

        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("\nFor more examples, see the 'examples/' directory.")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure to:")
        print("  1. Replace 'YOUR_API_KEY' with your actual API key")
        print("  2. Or set IPC_API_KEY environment variable")


if __name__ == "__main__":
    main()
