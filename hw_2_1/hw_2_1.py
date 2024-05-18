import sqlite3
import pandas as pd
from IPython.core.display_functions import display
import psycopg2.errors as pe 
from datetime import datetime

# З'єднання з базою даних SQLite
conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

# Створення таблиці users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Створення таблиці status
cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Створення таблиці tasks
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

# Збереження змін у базі даних
conn.commit()

# Запит на вибір завдань за user-id:
select_tasks_by_user_id = """
SELECT *FROM tasks WHERE user_id = ?;
"""
user_id = 6

# Запит на вибір завдань за статусом (status-id)
select_tasks_by_status = """
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);
"""

status_name = 'new' 

# Оновлення статусу завдання
update_task_status = """
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = ?)
WHERE id = ?;
"""
new_status = 'in progress'  # Новий статус для завдання
task_id = 8  # ID завдання, статус якого потрібно оновити

# Запит на вибір користувачів без завдань
select_users_without_tasks = """
SELECT id, fullname, email, created_at FROM users
WHERE id NOT IN (SELECT user_id FROM tasks);
"""

# Приклад даних для нового завдання
new_task_data = {
    'title': 'Veb-designer',
    'description': 'Creating vebpages',
    'status_id': 1,  # ID статусу нового завдання
    'user_id': 1  # ID користувача, для якого додається нове завдання
}

# Запит INSERT для додавання нового завдання
insert_new_task = """
INSERT INTO tasks (title, description, status_id, user_id, created_at)
VALUES (?, ?, ?, ?, ?);
"""

# Параметри для запиту INSERT
task_params = (
    new_task_data['title'],
    new_task_data['description'],
    new_task_data['status_id'],
    new_task_data['user_id'],
    datetime.now()  # Поточна дата і час для created_at
)

# Запит SELECT для отримання незавершених завдань
select_uncompleted_tasks = """
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
"""

# ID завдання, яке потрібно видалити
task_id_to_delete = 1  # Припустимо, що потрібно видалити завдання з ID 1

# Запит DELETE для видалення конкретного завдання за його ID
delete_task_by_id = """
DELETE FROM tasks
WHERE id = ?;
"""

# Електронна пошта, за якою проводиться пошук
search_email = 'erica30@example.net'  # Приклад: пошук всіх користувачів з електронною поштою, що закінчується на example.net

# Запит SELECT з умовою LIKE для фільтрації за електронною поштою
select_users_by_email = """
SELECT * FROM users
WHERE email LIKE ?;
"""

# ID користувача, для якого потрібно оновити ім'я
user_id_to_update = 1  # Припустимо, що потрібно оновити ім'я користувача з ID 1

# Нове ім'я користувача
new_username = 'Alex Korh'

# Запит UPDATE для оновлення імені користувача
update_username = """
UPDATE users
SET fullname = ?
WHERE id = ?;
"""

# Запит SELECT з операторами COUNT та GROUP BY для групування завдань за статусами
select_task_count_by_status = """
SELECT status.name, COUNT(tasks.id) AS task_count
FROM tasks
JOIN status ON tasks.status_id = status.id
GROUP BY status.name;
"""

# Доменна частина електронної пошти для пошуку
domain = '%@example.com'  # Приклад: пошук завдань, призначених користувачам з доменом example.com

# Запит SELECT з умовою LIKE в поєднанні з JOIN для вибору завдань, призначених користувачам з певною доменною частиною електронної пошти
select_tasks_by_email_domain = """
SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE ?;
"""

# Запит SELECT з умовою WHERE для вибору завдань, у яких відсутній опис
select_tasks_without_description = """
SELECT * FROM tasks
WHERE description IS NULL OR description = '';
"""

# Запит SELECT з INNER JOIN для вибору користувачів та їхніх завдань у статусі 'in progress'
select_users_tasks_in_progress = """
SELECT users.fullname, tasks.title
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';
"""

# Запит SELECT з LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань
select_users_task_count = """
SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.fullname;
"""

# Execution of creation, fiiling and selectionin tables as well as commiting commands
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
            
            # Відображення результатів у вигляді DataFrame без уточнення назв колонок
            if result:
                df= pd.DataFrame(result, columns=[x[0] for x in cursor.description])
                display(df)

                print(f"Статус завдання з ID {task_id} успішно оновлено на '{new_status}'.")
                print("Нове завдання успішно додане!")
                print(f"Завдання з ID {task_id_to_delete} успішно видалено!")
                print(f"Ім'я користувача з ID {user_id_to_update} успішно оновлено!")
            else: 
                print("Немає завдань без опису.")
                print("Немає користувачів з завданнями у статусі 'in progress'.")
                print("Немає даних для відображення.")
        except sqlite3.Error as e:
            print ("Помилка при виконанні запиту INSERT:", "Помилка при видаленні завдання:", "Помилка при оновленні імені користувача:", e)
            print("Немає користувачів з завданнями у статусі 'in progress'.")
            print("Немає даних для відображення.")
    else: 
        print("Error! cannot create the database connection.")
       

# Закриття з'єднання
cursor.close()
conn.close()

print("Таблиці успішно створено!")
