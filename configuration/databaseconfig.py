from configuration.api_response import get_response
import sqlite3, json, requests, logging

def fetch_users():
    try:
        response = get_response()
        if response.status_code == 200:
            users_data = response.json().get('results', [])
            return users_data  # Return the list of user dictionaries
        else:
            logging.error(f"Failed to fetch users: Received status code {response.status_code}")
            return []
    except requests.ConnectionError:
        logging.error("Failed to fetch users: Unable to connect to the website.")
        return []
    except requests.Timeout:
        logging.error("Failed to fetch users: The request timed out.")
        return []
    except Exception as e:
        logging.error(f"Failed to fetch users: An error occurred: {e}")
        return []



def send_to_database(data):
    conn = sqlite3.connect('mydatabase.sqlite')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS parents (
            formID INTEGER PRIMARY KEY AUTOINCREMENT,
            studentId INTEGER,
            institutionEmail TEXT,
            userName TEXT,
            password TEXT,
            gender TEXT,
            institutionRoleIds TEXT,
            systemRoleIds TEXT,
            availability TEXT,
            name TEXT,
            contact TEXT,
            birthDate DATE,
            job TEXT,
            address TEXT
        )
    ''')
    conn.commit()

    # Convert lists/dicts to JSON strings for specified fields, excluding institutionRoleIds
    json_fields = ["studentId", "institutionEmail", "userName", "password", "gender", 
                   "systemRoleIds", "availability", "name", "contact",
                   "birthDate", "job", "address"]

    for field in json_fields:
        if isinstance(data.get(field), (list, dict)):
            data[field] = json.dumps(data[field])

    # Convert institutionRoleIds to a string for database storage
    data['institutionRoleIds'] = json.dumps(data['institutionRoleIds'])

    cursor.execute('''INSERT INTO parents 
                      (studentId, institutionEmail, userName, password, gender, institutionRoleIds, systemRoleIds, 
                      availability, name, contact, birthDate, job, address) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (data.get("studentId"), data.get("institutionEmail"), data.get("userName"), data.get("password"), 
                    data.get("gender"), data.get("institutionRoleIds"), data.get("systemRoleIds"), 
                    data.get("availability"), data.get("name"), data.get("contact"), data.get("birthDate"), 
                    data.get("job"), data.get("address")))
    conn.commit()
    print("Parents data inserted successfully.")
    
    cursor.close()
    conn.close()

    return data