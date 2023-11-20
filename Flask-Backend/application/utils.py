from bcrypt import hashpw, gensalt, checkpw

def hash_password(plain_pw):
    salt = gensalt()
    return hashpw(plain_pw.encode('utf-8'),salt)

def check_password(plain_pw, hash_pw):
    return checkpw(plain_pw.encode('utf-8'),hash_pw)

