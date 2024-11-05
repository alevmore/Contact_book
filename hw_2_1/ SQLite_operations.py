import sqlite3
import pandas as pd
from IPython.core.display_functions import display
import psycopg2.errors as pe 
from datetime import datetime

# Connection to database SQLite
conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

# Creating table users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Creating table status
cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Creating table tasks
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
''')

# Saving changes in database 
conn.commit()

# Selecting tasks by user_id:
select_tasks_by_user_id = """
SELECT *FROM tasks WHERE user_id = ?;
"""
user_id = 6

# Selecting tasks by status-id
select_tasks_by_status = """
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);
"""

status_name = 'new' 

# Updation the task status
update_task_status = """
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = ?)
WHERE id = ?;
"""
new_status = 'in progress'  # Новий статус для завдання
task_id = 8  # task ID which should be updated 

# Selecting users without tasks 
select_users_without_tasks = """
SELECT id, fullname, email, created_at FROM users
WHERE id NOT IN (SELECT user_id FROM tasks);
"""

# Example of data for a new task 
new_task_data = {
    'title': 'Veb-designer',
    'description': 'Creating vebpages',
    'status_id': 1,  # ID статусу нового завдання
    'user_id': 1  # ID користувача, для якого додається нове завдання
}

# INSERT for adding a new task 
insert_new_task = """
INSERT INTO tasks (title, description, status_id, user_id, created_at)
VALUES (?, ?, ?, ?, ?);
"""

# Parameters for query INSERT
task_params = (
    new_task_data['title'],
    new_task_data['description'],
    new_task_data['status_id'],
    new_task_data['user_id'],
    datetime.now()  # Поточна дата і час для created_at
)

# SELECT for receiving unfinished tasks 
select_uncompleted_tasks = """
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
"""

# task ID, which should be deleted
task_id_to_delete = 1  # Припустимо, що потрібно видалити завдання з ID 1

# DELETE for deleting a particular task by its ID 
delete_task_by_id = """
DELETE FROM tasks
WHERE id = ?;
"""

# Searching users by their email address if it ends on example.net
search_email = 'erica30@example.net'  

# SELECT with condition LIKE for filtration by email address
select_users_by_email = """
SELECT * FROM users
WHERE email LIKE ?;
"""

# User ID for updating their name 
user_id_to_update = 1  

# New user name
new_username = 'Alex Korh'

# UPDATE for updating user name 
update_username = """
UPDATE users
SET fullname = ?
WHERE id = ?;
"""

# SELECT with operators COUNT та GROUP BY for grouping tasks by their status 
select_task_count_by_status = """
SELECT status.name, COUNT(tasks.id) AS task_count
FROM tasks
JOIN status ON tasks.status_id = status.id
GROUP BY status.name;
"""

# Domain part of the email to search for example.com
domain = '%@example.com'  

# SELECT query with LIKE condition in combination with JOIN to select tasks assigned to users with a specific email domain
select_tasks_by_email_domain = """
SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE ?;
"""

# SELECT query with a WHERE clause to select tasks that do not have a description
select_tasks_without_description = """
SELECT * FROM tasks
WHERE description IS NULL OR description = '';
"""

# SELECT query with INNER JOIN to select users and their tasks in the ‘in progress’ status
select_users_tasks_in_progress = """
SELECT users.fullname, tasks.title
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';
"""

# SELECT query with LEFT JOIN and GROUP BY to select users and count their tasks
select_users_task_count = """
SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.fullname;
"""

# Execution of creation, filing and selection tables as well as committing commands
with conn:
    if conn is not None:
        try: 
            cursor.execute(select_tasks_by_user_id, (user_id,))
            cursor.execute(select_tasks_by_status, (status_name,))
            cursor.execute(update_task_status, (new_status, task_id))
            cursor.execute(select_users_without_tasks)
            cursor.execute(insert_new_task, task_params)
            cursor.execute(select_uncompleted_tasks)
            cursor.execute(delete_task_by_id, (task_id_to_delete,))
            cursor.execute(select_users_by_email, ('%' + search_email,))
            cursor.execute(update_username, (new_username, user_id_to_update))
            cursor.execute(select_task_count_by_status)
            cursor.execute(select_tasks_by_email_domain, (domain,))
            cursor.execute(select_tasks_without_description)
            cursor.execute(select_users_tasks_in_progress)
            cursor.execute(select_users_task_count)

            conn.commit()
            result = cursor.fetchall()
            
            # Displaying results in the form of a DataFrame without specifying column names
            if result:
                df= pd.DataFrame(result, columns=[x[0] for x in cursor.description])
                display(df)

                print(f"Task status with ID {task_id} successfully updated to '{new_status}'.")
                print("New task added successfully!")
                print(f"Task with ID {task_id_to_delete} successfully deleted!")
                print(f"User name with ID {user_id_to_update} successfully updated!")
            else: 
                print("No tasks without a description.")
                print("No users with tasks in the status 'in progress'.")
                print("No data to display.")
        except sqlite3.Error as e:
            print ("Error when executing INSERT query:", "Помилка при видаленні завдання:", "Помилка при оновленні імені користувача:", e)
            print("No users with tasks in the status 'in progress'.")
            print("No data to display.")
    else: 
        print("Error! cannot create the database connection.")
       

# Close connection
cursor.close()
conn.close()

print("Tables created successfully!")
