import bcrypt

def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print(password)
    print(salt)
    print(hashed_password)
    return hashed_password.decode('utf-8')

def check_password_hash(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))