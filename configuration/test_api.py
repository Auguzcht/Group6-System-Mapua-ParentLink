from flask import redirect, url_for, jsonify, request
from configuration.appconfig import get_access_token
from configuration.sendemail import send_user_email
from configuration.api_response import get_response, post_response
from configuration.databaseconfig import send_to_database
import requests, logging

access_token = get_access_token

def fetch_users():
    try:
        response = get_response()

        if response.status_code == 200:
            users_data = response.json().get('results', [])
            if isinstance(users_data, list):
                users = [
                    f"Name: {user['name']['given']}, Username: {user['userName']}, Email: {user.get('contact', {}).get('email', 'N/A')}"
                    for user in users_data if isinstance(user, dict)
                ]
                return "<br>".join(users) if users else "No users found."
            else:
                logging.error("Unexpected data format: 'results' is not a list.")
                return "Failed to fetch users: Unexpected data format."
        else:
            logging.error(f"Failed to fetch users: Received status code {response.status_code}")
            logging.debug(f"Response content: {response.content}")
            return f"Failed to fetch users: Received status code {response.status_code}"
    except requests.ConnectionError:
        logging.error("Failed to fetch users: Unable to connect to the website.")
        return "Failed to fetch users: Unable to connect to the website."
    except requests.Timeout:
        logging.error("Failed to fetch users: The request timed out.")
        return "Failed to fetch users: The request timed out."
    except Exception as e:
        logging.error(f"Failed to fetch users: An error occurred: {e}")
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

def test_create_user():
    user_data = {
        "studentId": "2411234",
        "institutionEmail": "sample@mcm.edu.ph",
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
    
    send_user_email(user_data)
    send_to_database(user_data)
    

    try:
        # Send POST request to the API endpoint
        response = post_response(user_data, access_token)
        
        # Check if the user creation was successful
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            # Log the error response for debugging
            print(f"Failed to create user: {response.status_code} - {response.text}")
            return redirect(url_for('index'))

    except requests.ConnectionError:
        return jsonify({"error": "Failed to create user: Unable to connect to the website."}), 500
    except requests.Timeout:
        return jsonify({"error": "Failed to create user: The request timed out."}), 504
    except Exception as e:
        return jsonify({"error": f"Failed to create user: An error occurred: {str(e)}"}), 500