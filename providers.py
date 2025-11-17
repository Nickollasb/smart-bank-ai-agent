import requests

#TODO: Add error handling and logging
def http_request(method: str, url: str) -> dict:
    """Make an HTTP request to a given URL and return the response on JSON."""
    try:
        response = requests.request(method, url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None