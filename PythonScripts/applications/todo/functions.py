import sqlite3


def insert_task(conn, cursor, task):
    with conn:
        sql = "insert into tasks ('description', 'done', 'date') values (?, ?, ?)"
        values = (task.description, task.done, task.date)
        cursor.execute(sql, values)
    return


def get_task(cursor, id):
    sql = "select * from tasks where id=?"
    values = (id)
    cursor.execute(sql, values)
    return cursor.fetchall()


def get_all_undone_tasks(cursor):
    sql = "select * from tasks where done=0"
    cursor.execute(sql)
    return cursor.fetchall()


def get_all_done_tasks(cursor):
    sql = "select * from tasks where done=1"
    cursor.execute(sql)
    return cursor.fetchall()

def get_all(cursor):
    done_tasks = get_all_done_tasks(cursor)
    undone_tasks = get_all_undone_tasks(cursor)

    return done_tasks, undone_tasks


def mark_task_done(conn, cursor, id):
    with conn:
        sql = "update tasks set done=1 where id=?"
        values = (id)
        cursor.execute(sql, values)
    return


def mark_task_undone(conn, cursor, id):
    with conn:
        sql = "update tasks set done=0 where id=?"
        values = (id)
        cursor.execute(sql, values)
    return


def delete_task(conn, cursor, id):
    with conn:
        sql = "delete from tasks where id=?"
        values = (id)
        cursor.execute(sql, values)
    return


def delete_all_done_tasks(conn, cursor):
    with conn:
        sql = "delete from tasks where done=1"
        cursor.execute(sql)

    return


def delete_topic(conn, cursor, id):
    with conn:
        sql = "delete from topics where id=?"
        values = (id)
        cursor.execute(sql, values)
    return


def create_table(conn, cursor, entity):
    if entity == "tasks":
        create_tasks_table(conn, cursor)
    elif entity == "topics":
        create_topics_table(conn, cursor)
    else:
        print("Unknown Entity")

    return


def create_tasks_table(conn, cursor):
    with conn:
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            description TEXT,
                            done INTEGER DEFAULT 0,
                            date TEXT
                            )""")

    return


def create_topics_table(conn, cursor):
    with conn:
        cursor.execute("""CREATE TABLE IF NOT EXISTS topics (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            description TEXT,
                            tasks TEXT,
                            date TEXT
                            )""")

    return


def create_topic(conn, cursor, topic):
    with conn:
        sql = "insert into topics ('description', 'date', 'tasks') values (?, ?, ?)"
        values = (topic.get_description(), topic.get_date(), topic.get_tasks())
        cursor.execute(sql, values)

    return


def add_tasks_to_topic(conn, cursor, list_of_tasks, topic_id):
    with conn:
        tasks_string = ""
        for task in list_of_tasks:
            tasks_string += str(task) + " "
        print(tasks_string)

        sql = "update topics set tasks=tasks||(?) where id=?"
        print(sql)
        values = (tasks_string, topic_id)
        cursor.execute(sql, values)

    return


def get_all_tasks_in_topic(cursor, topic_id):
    sql = "select tasks from topics where id=?"
    values = (str(topic_id))
    cursor.execute(sql, values)

    tasks_string = cursor.fetchone()[0]
    if not tasks_string:
        return []

    tasks_array = tasks_string.split(" ")

    tasks_comma_delimited_string = ""
    for i, task in enumerate(tasks_array):
        if i and task:
            tasks_comma_delimited_string += ","
        tasks_comma_delimited_string += task

    sql = "select * from tasks where id in (" + tasks_comma_delimited_string + ")"
    cursor.execute(sql)
    tasks = cursor.fetchall()
    return tasks


def get_all_topics(cursor):
    sql = "select * from topics"
    cursor.execute(sql)

    return cursor.fetchall()


def get_all_topics_with_tasks(cursor):
    topics = get_all_topics(cursor)
    topic_with_tasks = []

    for topic in topics:
        tasks = get_all_tasks_in_topic(cursor, topic[0])
        topic_task = {
            'topic': topic,
            'tasks': tasks
        }

        topic_with_tasks.append(topic_task)

    return topic_with_tasks


def get_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def close_connection(conn):
    conn.close()
