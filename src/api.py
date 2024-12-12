import requests
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
import time

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def create_session():
    """Create a requests session with retry logic"""
    session = requests.Session()
    
    # Configure retry strategy
    retries = Retry(
        total=3,  # total number of retries
        backoff_factor=1,  # wait 1, 2, 4 seconds between retries
        status_forcelist=[408, 429, 500, 502, 503, 504],  # retry on these status codes
        allowed_methods=["GET"]  # only retry on GET requests
    )
    
    # Add retry adapter to session
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def make_api_request(url, params=None, auth=None, timeout=(5, 15)):
    """Generic API request handler with error handling"""
    session = create_session()
    try:
        response = session.get(
            url,
            params=params,
            auth=auth,
            timeout=timeout  # (connect timeout, read timeout)
        )
        
        # Log non-200 responses
        if response.status_code != 200:
            print(f"API request failed at {datetime.now()}")
            print(f"URL: {url}")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")  # First 200 chars of response
            
        return response
        
    except requests.exceptions.ConnectTimeout:
        raise APIError(f"Connection timeout while connecting to {url}")
    except requests.exceptions.ReadTimeout:
        raise APIError(f"Read timeout while reading from {url}")
    except requests.exceptions.ConnectionError:
        raise APIError(f"Connection error while connecting to {url}")
    except requests.exceptions.RequestException as e:
        raise APIError(f"Unexpected error during API request: {str(e)}")
    finally:
        session.close()

def build_api_url(address, port, endpoint):
    """Safely build API URL"""
    if not address or not port or not endpoint:
        raise APIError("Missing required parameters for URL construction")
    return f"http://{address}:{port}/api/v5/{endpoint}"

def call_api_clients(address, port, cluster_user, cluster_password):
    """Call clients API endpoint with error handling"""
    try:
        url = build_api_url(address, port, "clients")
        params = {"like_clientid": "sub"}
        
        if not cluster_user or not cluster_password:
            raise APIError("Missing authentication credentials")
            
        return make_api_request(
            url=url,
            params=params,
            auth=(cluster_user, cluster_password)
        )
        
    except APIError as e:
        print(f"Error in call_api_clients at {datetime.now()}: {str(e)}")
        # Return a dummy response object with error status
        return type('Response', (), {'status_code': 500, 'text': str(e)})
    except Exception as e:
        print(f"Unexpected error in call_api_clients at {datetime.now()}: {str(e)}")
        return type('Response', (), {'status_code': 500, 'text': str(e)})

def call_api_nodes(address, port, cluster_user, cluster_password):
    """Call nodes API endpoint with error handling"""
    try:
        url = build_api_url(address, port, "nodes")
        
        if not cluster_user or not cluster_password:
            raise APIError("Missing authentication credentials")
            
        return make_api_request(
            url=url,
            auth=(cluster_user, cluster_password)
        )
        
    except APIError as e:
        print(f"Error in call_api_nodes at {datetime.now()}: {str(e)}")
        # Return a dummy response object with error status
        return type('Response', (), {'status_code': 500, 'text': str(e)})
    except Exception as e:
        print(f"Unexpected error in call_api_nodes at {datetime.now()}: {str(e)}")
        return type('Response', (), {'status_code': 500, 'text': str(e)})