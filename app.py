from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from configuration.api_database import *
from configuration.sendemail import *
from configuration.api_response import post_response, observer_response
from configuration.test_api import fetch_users, use_api, test_email, test_create_user
from configuration.submitform import contact_form, registration_form
from configuration.databaseconfig import send_to_database

import requests

app = Flask(__name__)
load_dotenv()


access_token = get_access_token()

# Fetch users to automatically transfer to database (if successfully connected to API)
if access_token:
    print("Connected to Blackboard API")
    fetch_users_to_database()

#Website Page Routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/terms_and_privacy')
def terms_and_privacy_page():
    return render_template("content.html")

@app.route('/register')
def register_page():
    return render_template("register.html", access_token=access_token)

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

    observer = request.form.get('username')
    student = request.form.get('student-id')

    try:
        print("Uploading to BlackBoard API...")
        response_post = post_response(user_data, access_token)
        
        if response_post.status_code == 201:
            print(f"User created successfully: {response_post.status_code}")
            send_to_database(user_data)
            observer_response(student, observer)
            return redirect(url_for('index'))
        else:
            print(f"Failed to create user: {response_post.status_code} - {response_post.text}")
            send_to_database(user_data)
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
def test_create_user_page():
    return test_create_user()

    
if __name__ == '__main__':
    app.run(debug=True)
