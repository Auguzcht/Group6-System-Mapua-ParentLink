from configuration.appconfig import get_access_token
import requests

access_token = get_access_token()

def get_response():
    response = requests.get(
        'https://malayanmindanao-test.blackboard.com/learn/api/public/v1/users',  # Replace with actual user API endpoint
        timeout=5,
        headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'})
    
    return response

def post_response(fetched_data, access_token):
    response = requests.post(
        'https://malayanmindanao-test.blackboard.com/learn/api/public/v1/users',
        timeout=5,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=fetched_data
    )
    
    return response

def observer_response(userId, observerId):
    response = requests.put(
        f'https://malayanmindanao-test.blackboard.com/learn/api/public/v1/users/userName:{userId}/observers/userName:{observerId}',
        timeout=5,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        data = {
        "userId": userId,
        "observerId": observerId,
        }
    )

    if response.status_code == 201:
        print(f"User assigned to observer successfully.")

    else:
        print(f"Failed to assign observer: {response.status_code} - {response.text}")

    return response