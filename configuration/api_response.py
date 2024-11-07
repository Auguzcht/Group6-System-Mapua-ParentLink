from configuration.appconfig import get_access_token
import requests

access_token = get_access_token

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