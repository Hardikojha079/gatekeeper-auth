import bcrypt

customers = [
    {"account_number": 345678912345, "password": "Password1"},
    {"account_number": 456789123456, "password": "Password2"},
    {"account_number": 567891234567, "password": "Password3"},
    {"account_number": 678912345678, "password": "Password4"},
    {"account_number": 789123456789, "password": "Password5"},
    {"account_number": 891234567890, "password": "Password6"},
    {"account_number": 912345678901, "password": "Password7"},
    {"account_number": 123456789012, "password": "Password8"},
    {"account_number": 234567890123, "password": "Password9"},
    {"account_number": 234567891234, "password": "Password10"},
]

for customer in customers:
    password = customer["password"]
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    print(f"Account Number: {customer['account_number']}, Hashed Password: {hashed_password_str}")