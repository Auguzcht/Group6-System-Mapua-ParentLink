from configuration.api_response import get_response, post_response
from configuration.databaseconfig import fetch_users
from configuration.appconfig import get_access_token
from configuration.error_checking import user_exists
import sqlite3, json, logging

access_token = get_access_token()

def fetch_users_to_database():
    logging.info("Fetching users to database...")
    users = fetch_users()

    with sqlite3.connect('mydatabase.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                formId INTEGER PRIMARY KEY AUTOINCREMENT,
                studentId INTEGER,
                institutionEmail TEXT,
                userName TEXT UNIQUE,
                password TEXT,
                gender TEXT,
                institutionRoleIds TEXT,
                systemRoleIds TEXT,
                availability TEXT,
                name TEXT,
                contact TEXT
            )
        ''')

        for user in users:
            institutionRoleIds = json.dumps(user.get('institutionRoleIds', []))
            systemRoleIds = json.dumps(user.get('systemRoleIds', []))
            availability = json.dumps(user.get('availability', {}))
            name = json.dumps(user.get('name', {}))
            contact = json.dumps(user.get('contact', {}))

            cursor.execute(''' 
                INSERT OR REPLACE INTO users (studentId, userName, institutionRoleIds, systemRoleIds, availability, name, contact)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.get('studentId'),
                user.get('userName'),
                institutionRoleIds,
                systemRoleIds,
                availability,
                name,
                contact
            ))

        conn.commit()



def fetch_parents_from_database_to_api():
    try:
        fetched_data = None
        users = fetch_users()
        conn = sqlite3.connect('mydatabase.sqlite')
        cursor = conn.cursor()
        for user in users:
            cursor.execute('''SELECT studentId, institutionEmail, userName, password, gender, institutionRoleIds, systemRoleIds, 
                              availability, name, contact FROM users WHERE userName = ?''', 
                           (user["userName"],))
            row = cursor.fetchone()
            if not row:
                print(f"No user found in the database for userName: {user['userName']}.")
                continue
            check_get_response = get_response()
            if check_get_response.status_code == 200:
                fetched_data = {
                    "studentId": row[0],
                    "institutionEmail": row[1],
                    "userName": row[2],
                    "password": row[3],
                    "gender": row[4],
                    "institutionRoleIds": json.loads(row[5]) if row[5] else None,
                    "systemRoleIds": json.loads(row[6]) if row[6] else None,
                    "availability": json.loads(row[7]) if row[7] else None,
                    "name": json.loads(row[8]) if row[8] else None,
                    "contact": json.loads(row[9]) if row[9] else None
                }
                if user_exists(fetched_data['userName']):
                    print(f"User {fetched_data['userName']} already exists in the API. No insertion done.")
                else:
                    post_response(fetched_data, access_token)  # Pass the access_token here
                    print(f"Data for user {fetched_data['userName']} imported successfully.")
            else:
                print("Failed to fetch data from the API.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return fetched_data