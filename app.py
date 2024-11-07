from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from configuration.sqlite import *
from configuration.sendemail import *
from configuration.appconfig import get_access_token
from configuration.api_response import post_response
from configuration.test_api import fetch_users, use_api, test_email
from configuration.submitform import contact_form, registration_form
import requests

app = Flask(__name__)
load_dotenv()

access_token = get_access_token()

# Fetch users to automatically transfer to database (if successfully connected to API)
if access_token:
    users = fetch_users()
    fetch_users_to_database(users)
    fetch_users_from_database_to_api(users)

#Website Page Routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/terms_and_privacy')
def terms_and_privacy_page():
    return render_template("content.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

# POST Method Routes
@app.route('/submit_contact_form', methods=["POST"])
def submit_contact_form():
    form = contact_form()
    send_contact_email(form)

    return redirect(url_for('index') + "#contact-section")

@app.route('/submit_registration_form', methods=["POST"])
def submit_registration_form():
    user_data = registration_form()
    
    send_user_email(user_data)
    send_to_database(user_data)

    try:
        print("Uploading to BlackBoard API...")
        response = post_response(user_data, access_token)
        
        if response.status_code == 201:
            print(f"User created successfully: {response.status_code}")
            return redirect(url_for('index'))
        else:
            print(f"Failed to create user: {response.status_code} - {response.text}")
            return redirect(url_for('index'))

    except requests.ConnectionError:
        return jsonify({"error": "Failed to create user: Unable to connect to the website."}), 500
    except requests.Timeout:
        return jsonify({"error": "Failed to create user: The request timed out."}), 504
    except Exception as e:
        return jsonify({"error": f"Failed to create user: An error occurred: {str(e)}"}), 500


# BEYOND THIS POINT ARE ROUTES TO TEST BLACKBOARD API OR FORM SUBMISSIONS #
@app.route('/use_api')
def use_api_page():
    return use_api()

@app.route('/fetch_users')
def fetch_users_page():
    return fetch_users()

@app.route('/test_email')
def test_email_page():
    return test_email()

@app.route('/test_create_user')
def test_create_user():
    user_data = {
        "studentID": "2411234",
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
    
    user_data = request.json

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

    
if __name__ == '__main__':
    app.run(debug=True)
