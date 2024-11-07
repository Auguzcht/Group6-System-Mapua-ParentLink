from configuration.appconfig import get_access_token
from configuration.sendemail import send_user_email
from configuration.api_response import get_response
import requests, logging

access_token = get_access_token

def fetch_users():
    try:
        response = get_response()

        if response.status_code == 200:
            users_data = response.json().get('results', [])  # Extract 'results' list
            # Format user data for display
            users = [
                f"Name: {user['name']['given']}, Username: {user['userName']}, Email: {user.get('contact', {}).get('email', 'N/A')}"
                for user in users_data
            ]

            return "<br>".join(users) if users else "No users found."
        else:
            return f"Failed to fetch users: Received status code {response.status_code}"
        

    except requests.ConnectionError:
        return "Failed to fetch users: Unable to connect to the website."
    except requests.Timeout:
        return "Failed to fetch users: The request timed out."
    except Exception as e:
        return f"Failed to fetch users: An error occurred: {e}"

def use_api():    
    try:
        response = get_response()

        if response.status_code == 200:
            return "Ping successful: The website is reachable!"
        else:
            return f"Ping failed: Received status code {response.status_code}"
    
    except requests.ConnectionError:
        return "Ping failed: Unable to connect to the website."
    except requests.Timeout:
        return "Ping failed: The request timed out."
    except Exception as e:
        return f"Ping failed: An error occurred: {e}"

logging.basicConfig(level=logging.DEBUG)

def test_email():
    sample_data = {
        "userName": "sample",
        "password": "yes",
        "gender": "Male",
        "institutionRoleIds": ["STUDENT"],
        "systemRoleIds": ["User"],
        "availability": {"available": "Yes"},
        "name": {
            "given": "Sample",
            "family": "Text",
            },
        "contact": {
            "email": "micobarrios@gmail.com"
            }
    }
    
    send_user_email(sample_data)
    
    return "Email sent"