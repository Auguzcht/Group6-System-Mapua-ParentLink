from flask import request


def contact_form():
    contact_name = request.form.get('contact-name')
    user_email = request.form.get('user-email')
    admin_email = request.form.get('admin-email')
    message = request.form.get('message')

    contact_data = {
        'contact_name': contact_name,
        'user_email': user_email,
        'admin_email': admin_email,
        'message': message
    }

    return contact_data

def registration_form():
    first_name = request.form.get('first-name')
    middle_name = request.form.get('middle-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    gender = request.form.get('gender')
    birth_date = request.form.get('birth-date')
    company = request.form.get('company')
    street = request.form.get('street')
    city = request.form.get('city')

    student_id = request.form.get('student-id')
    #student_email = request.form.get('student-email')
    
    print(f"First Name: {first_name}, Middle Name: {middle_name}, Last Name: {last_name}")
    print(f"Email: {email}, Username: {username}, Password: {password}")
    print(f"Gender: {gender}, Birth Date: {birth_date}, Company: {company}")
    print(f"Street: {street}, City: {city}, Student ID: {student_id}")
    
    if middle_name is None:
        registration_data = {
            'studentID': student_id,
            'userName': username,
            'password': password,
            'gender': gender,
            'institutionRoleIds': ["OBSERVER"],
            'systemRoleIds': ["User"],
            'availability': {"available": "Yes"},
            'name': {
                'given': f"{first_name}",
                'family': last_name,
                },
            'contact': {
                "email": email
                },
            'birthDate': birth_date,
            'company': company,
            'street': street,
            'city': city
        }

        return registration_data
    
    else:
        registration_data = {
            'studentID': student_id,
            'userName': username,
            'password': password,
            'gender': gender,
            'institutionRoleIds': ["OBSERVER"],
            'systemRoleIds': ["User"],
            'availability': {"available": "Yes"},
            'name': {
                'given': f"{first_name}, {middle_name}",
                'family': last_name,
                },
            'contact': {
                "email": email
                },
            'birthDate': birth_date,
            'company': company,
            'street': street,
            'city': city
        }

        return registration_data