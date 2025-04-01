import bcrypt

def verify_password(stored_hash, entered_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8'))

stored_hash = "$2b$12$4lKrjdXnPteoZy4rIl0V5uN6ii.XmRJoQ8w6iPuDEcuMDyZFf.4RK" 
entered_password = "Password1"

if verify_password(stored_hash, entered_password):
    print("Password is correct!")
else:
    print("Incorrect password!")
