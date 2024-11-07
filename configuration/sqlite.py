from configuration.api_response import get_response, post_response
from configuration.appconfig import get_access_token
from configuration.error_checking import user_exists
import sqlite3, json

access_token = get_access_token()

def fetch_users_to_database(users):
    
    print("Fetching users to database...")
    
    conn = sqlite3.connect('mydatabase.sqlite')
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            formId INTEGER PRIMARY KEY AUTOINCREMENT,
            studentId INTEGER,
            institutionEmail TEXT,
            userName TEXT,
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

        # Insert into the table with the converted JSON values
        cursor.execute(''' 
            INSERT OR REPLACE INTO users (studentId, userName, institutionRoleIds, systemRoleIds, availability, name, contact)
            VALUES (?, ?, ?, ?, ?, ?, ())
        ''', (
            user.get('studentId'),
            user.get('userName'),
            institutionRoleIds,  # Use the JSON string
            systemRoleIds,       # Use the JSON string
            availability,        # Use the JSON string
            name,                # Use the JSON string
            contact              # Use the JSON string
        ))

    conn.commit()  # Commit the changes to the database
    cursor.close()
    conn.close()


def send_to_database(data):
    conn = sqlite3.connect('mydatabase.sqlite')
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS parents (
            formID INTEGER PRIMARY KEY AUTOINCREMENT,
            studentID INTEGER,
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
            company TEXT,
            street TEXT,
            city TEXT
        )
    ''')
    conn.commit()

    # Fields that may need JSON conversion
    json_fields = ["studentID", "institutionEmail", "userName", "password", "gender", "institutionRoleIds", 
                   "systemRoleIds", "availability", "name", "contact",
                   "birthDate", "company", "street", "city"]

    # Convert lists/dicts to JSON strings for specified fields
    for field in json_fields:
        if isinstance(data.get(field), (list, dict)):
            data[field] = json.dumps(data[field])

    # Insert the data into the database
    cursor.execute('''INSERT INTO parents 
                          (studentID, institutionEmail, userName, password, gender, institutionRoleIds, systemRoleIds, 
                          availability, name, contact, birthDate, company, street, city) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data.get("studentID"), data.get("institutionEmail"), data.get("userName"), data.get("password"), 
                        data.get("gender"), data.get("institutionRoleIds"), data.get("systemRoleIds"), 
                        data.get("availability"), data.get("name"), data.get("contact"), data.get("birthDate"), 
                        data.get("company"), data.get("street"), data.get("city")))

    conn.commit()
    print("Data inserted successfully.")
    
    cursor.close()
    conn.close()

    return data


def fetch_users_from_database_to_api(users):
    try:
        conn = sqlite3.connect('mydatabase.sqlite')
        cursor = conn.cursor()

        cursor.execute('''SELECT studentID, institutionEmail, userName, password, gender, institutionRoleIds, systemRoleIds, 
                          availability, name, contact FROM parents WHERE userName = ?''', 
                       (users["userName"],))
        row = cursor.fetchone()

        if not row:
            print("No user found in the database.")
            return None

        check_get_response = get_response()

        if check_get_response.status_code == 200:
            fetched_data = {
                "studentID": row[0],
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
                print("User already exists in the API. No insertion done.")
            else:
                post_response(fetched_data)
                print("Data imported successfully.")

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