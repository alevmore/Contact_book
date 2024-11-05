import sqlite3
from faker import Faker
import random
from datetime import datetime

# Connecting to a SQLite database
conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

# Initialisation Faker
fake = Faker()

# Filling in the users table
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cursor.execute('''
        INSERT INTO users (fullname, email, created_at) 
        VALUES (?, ?, ?)
    ''', (fullname, email, datetime.now()))

# Filling in the status table
status_names = ['new', 'in progress', 'completed']
for status_name in status_names:
    cursor.execute('''
        INSERT INTO status (name, created_at) 
        VALUES (?, ?)
    ''', (status_name, datetime.now()))

# Filling in the tasks table
for _ in range(20):
    title = fake.job()
    description = fake.text()
    status_id = random.randint(1, len(status_names))
    user_id = random.randint(1, 10)
    cursor.execute('''
        INSERT INTO tasks (title, description, status_id, user_id, created_at) 
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, status_id, user_id, datetime.now()))

# Saving changes in database 
conn.commit()

# Close connection
conn.close()

print("Data successfully filled in!")
