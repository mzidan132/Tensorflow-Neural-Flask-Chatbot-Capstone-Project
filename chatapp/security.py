import hashlib

# Temporary password
password = "123"

# Hash the password using SHA-256
hashed_password = hashlib.sha256(password.encode()).hexdigest()

print(hashed_password)
