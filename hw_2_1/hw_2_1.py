import psycopg2
import pandas as pd
from IPython.core.display_functions import display
import psycopg2.errors as pe  

# 1. Creating tables
create_table_status = """
CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
  );
"""
create_table_users = """
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100),
  email VARCHAR (100) UNIQUE
  );
"""
create_table_tasks = """
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(50),
  description TEXT,
  status_id INTEGER,
  id INTEGER,
  FOREIGN KEY (id) REFERENCES users(id),
  FOREIGN KEY (status_id) REFERENCES status(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
"""
# 2. Filling up tables
fill_table_status = """
INSERT INTO status (id, name)
VALUES (1, 'new'), (2, 'in progress'), (3, 'completed');
"""
fill_table_users = """
INSERT INTO users (id, fullname, email)
VALUES (1, 'Alla Morenko', 'fsgs@gmail.com'), (2, 'Oleh Konovalec', 'khjg@gmail.com'), (3, 'OLha Falion', 'vbnv@gmail.com'), (4, 'Dmytro Korzhyk', 'zczvc@gmail.com');
"""
fill_table_tasks = """
INSERT INTO tasks (id, title, description, status_id)
VALUES (1, 'analyst', 'perform data analysis', 1), (2, 'ingeneer', 'create softs', 2), (3, 'web designer', 'design of websites', 3), (4, 'fullstack developer', 'frontend developing', 2);
"""
# 3. SELECT info
select_tasks_by_id = """
SELECT * FROM tasks WHERE id IN (SELECT id FROM users WHERE id=2); """
select_task_by_status_id = """
SELECT * FROM tasks WHERE status_id IN (SELECT id
    FROM status WHERE id =1);
"""
update_status_id= """
UPDATE tasks SET status_id = 2 WHERE id =1;
"""
select_users_without_tasks = """
SELECT *FROM users
WHERE id NOT IN (SELECT id FROM tasks);
"""
insert_tasks = """
INSERT INTO tasks (id, title, description, status_id)
VALUES (5,'backend developer', 'applications', 1);
"""
select_uncompleted_tasks = """
SELECT * FROM tasks WHERE status_id IN (1,2)
"""
delete_tasks_by_id = """
DELETE FROM tasks WHERE id = 5;
"""
select_email = """
SELECT email FROM users
WHERE email LIKE 'zczvc@gmail.com'
ORDER BY fullname;
"""
update_name= """
UPDATE users SET fullname = 'Taras Shevchenko' WHERE id =1;
"""
count_by_status_id= """
SELECT COUNT(id) as total_users, 
status_id FROM tasks
GROUP BY status_id;
"""
select_tasks_by_email= """
SELECT u.fullname, u.email IN (SELECT email FROM users WHERE email LIKE 'gmail.com'), t.description AS tasks
FROM users AS u
INNER JOIN tasks AS t ON t.id = u.id;
"""
select_null_description= """
SELECT * FROM tasks WHERE description LIKE '%0%'; 
"""
select_user_in_progress= """
SELECT u.fullname, u.email, t.status_id IN(SELECT status_id FROM tasks WHERE status_id=2) AS tasks
FROM users AS u
INNER JOIN tasks AS t ON t.id = u.id;
"""
count_tasks_by_left_join = """
SELECT t.title, t.id, u.id AS users
FROM tasks AS t
INNER JOIN users AS u ON u.id = t.id
SELECT COUNT(tasks.id) as total_tasks, 
tasks.id FROM tasks
GROUP BY tasks.id;
"""
# 4. Connecting 
try:
  connection = psycopg2.connect(
    database="", user='postgres',
    password='Mysecretepassword', host='localhost', port=5432
  )

  cursor = connection.cursor()
except pe
  print (pe)


# 5. Execution of creztion, fiiling and selectionin tables as well as commiting commands
with connection as conn:
  if conn is not None:
    try: 
      cursor.execute(create_table_status)
      cursor.execute(create_table_users)
      cursor.execute(create_table_tasks)
      cursor.execute(fill_table_status)
      cursor.execute(fill_table_users)
      cursor.execute(fill_table_tasks)
      cursor.execute(select_tasks_by_id)
      cursor.execute(select_task_by_status_id)
      cursor.execute(update_status_id)
      cursor.execute(select_users_without_tasks)
      cursor.execute(insert_tasks)
      cursor.execute(select_uncompleted_tasks)
      cursor.execute(delete_tasks_by_id)
      cursor.execute(select_email)
      cursor.execute(update_name)
      cursor.execute(count_by_status_id)
      cursor.execute(select_tasks_by_email)
      cursor.execute(select_null_description)
      cursor.execute(select_user_in_progress)
      cursor.execute(count_tasks_by_left_join)
      connection.commit()
      result = cursor.fetchall()
      display (pd.DataFrame(result))
    except pe:
      print (pe)

  else: print("Error! cannot create the database connection.")


cursor.close()
connection.close()

