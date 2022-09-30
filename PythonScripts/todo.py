import sys
from colorama import Fore, init, Style, Back
import datetime
from applications.todo.models import Task, Topic
from applications.todo import functions
from utils import utils

init(autoreset=True)


COMMAND_NAME = ""
DB_NAME = "todo.db"

AVAILABLE_OPTIONS = {
    '-createtask': {
        'arg_required': False,
        'description': 'Creates a new Task'
    },
    '-d': {
        'arg_required': False,
        'description': 'gives description of the command'
    },
    '-deletetask': {
        'arg_required': True,
        'description': 'Deletes a specific task'
    },
    '-deletetopic': {
        'arg_required': True,
        'description': 'Deletes a specific topic'
    },
    '-done': {
        'arg_required': True,
        'description': 'Marks a specific Task as done'
    },
    '-undone': {
        'arg_required': True,
        'description': 'Marks a specific Task as undone'
    },
    '-getall': {
        'arg_required': False,
        'description': 'Gives the list of all the Tasks'
    },
    '-get': {
        'arg_required': True,
        'description': 'Gets a specific Task'
    },
    '-getdone': {
        'arg_required': False,
        'description': 'Gets all the Tasks which are marked as done'
    },
    '-getundone': {
        'arg_required': False,
        'description': 'Gets all the Tasks which are marked as undone'
    },
    '-cleardone': {
        'arg_required': False,
        'description': 'Deletes all the tasks that are marked done'
    },
    '-createtable': {
        'arg_required': True,
        'description': 'Creates a new table for a specific Entity'
    },
    '-createtopic': {
        'arg_required': False,
        'description': 'Creates a new Topic'
    },
    '-addtasktotopic': {
        'arg_required': False,
        'description': 'Creates a new Topic'
    },
    '-getalltopics': {
        'arg_required': False,
        'description': 'Gets all topics'
    },
    '-getever': {
        'arg_required': False,
        'description': 'Gets all the topics with tasks'
    },

}

def create_task():
    description = input("Enter task descrition: ")
    done = 0
    date = datetime.datetime.now().isoformat()

    return Task(1, description, done, date)


def create_topic():
    description = input("Enter topic descrition: ")
    tasks = ""
    date = datetime.datetime.now().isoformat()

    return Topic(1, description, tasks, date)


def add_task_to_topic(conn, cursor):
    topic_id = input("Enter topic id: ")
    task_id =  input("Enter task ids (space separated): ")

    tasks_array = task_id.split(" ")
    print(tasks_array)

    functions.add_tasks_to_topic(conn, cursor, tasks_array, topic_id)


def print_tasks(tasks):
    for task in tasks:
        id = task[0]
        description = task[1]
        done = int(task[2])
        date = task[3]

        if done == 0:
            print(f"{Fore.CYAN}{id}   {Fore.YELLOW}{date}   {Fore.WHITE}{description}")
        elif done == 1:
            print(f"{Fore.CYAN}{id}   {Fore.YELLOW}{date}   {Fore.LIGHTGREEN_EX}{description}")


def print_topics(topics):
    for topic in topics:
        id = topic[0]
        description = topic[1]
        tasks = topic[2]
        date = topic[3]

        print(f"{Fore.CYAN}{id}   {Fore.YELLOW}{date}   {Fore.WHITE}{description}   {Fore.LIGHTGREEN_EX}({tasks})")


def print_topics_with_tasks(topic_with_tasks):
    for topic_tasks in topic_with_tasks:
        topic = topic_tasks['topic']
        tasks = topic_tasks['tasks']

        topic_id = topic[0]
        description = topic[1]
        date = topic[3]
        print(f"{Fore.CYAN}{topic_id}   {Fore.YELLOW}{date}   {Fore.WHITE}{description}")

        for task in tasks:
            id = task[0]
            description = task[1]
            done = int(task[2])
            date = task[3]

            if done == 0:
                print(f"    {Fore.CYAN}{id}   {Fore.YELLOW}{date}   {Fore.WHITE}{description}")
            elif done == 1:
                print(f"    {Fore.CYAN}{id}   {Fore.YELLOW}{date}   {Fore.LIGHTGREEN_EX}{description}")

        print("\n")


def execute_cmd(options):
    conn = functions.get_connection(DB_NAME)
    cursor = conn.cursor()

    if '-d' in options:
        utils.print_description(COMMAND_NAME, AVAILABLE_OPTIONS)
    elif '-createtask' in options:
        task = create_task()
        functions.insert_task(conn, cursor, task)
    elif '-createtopic' in options:
        topic = create_topic()
        functions.create_topic(conn, cursor, topic)
    elif '-addtasktotopic' in options:
        add_task_to_topic(conn, cursor)
    elif '-deletetask' in options:
        task_id = options['-deletetask']
        functions.delete_task(conn, cursor, task_id)
    elif '-deletetopic' in options:
        task_id = options['-deletetopic']
        functions.delete_topic(conn, cursor, task_id)
    elif '-done' in options:
        task_id = options['-done']
        functions.mark_task_done(conn, cursor, task_id)
    elif '-undone' in options:
        task_id = options['-undone']
        functions.mark_task_undone(conn, cursor, task_id)
    elif '-get' in options:
        task_id = options['-get']
        task = functions.get_task(cursor, task_id)
        print_tasks(task)
    elif '-getdone' in options:
        tasks = functions.get_all_done_tasks(cursor)
        print_tasks(tasks)
    elif '-getundone' in options:
        tasks = functions.get_all_undone_tasks(cursor)
        print_tasks(tasks)
    elif '-createtable' in options:
        functions.create_table(conn, cursor, options['-createtable'])
    elif '-getall' in options:
        done_tasks, undone_tasks = functions.get_all(cursor)
        print_tasks(done_tasks)
        print_tasks(undone_tasks)
    elif '-getalltopics' in options:
        topics = functions.get_all_topics(cursor)
        print_topics(topics)
    elif '-getever' in options:
        topic_with_tasks = functions.get_all_topics_with_tasks(cursor)
        print_topics_with_tasks(topic_with_tasks)
    elif '-cleardone' in options:
        functions.delete_all_done_tasks(conn, cursor)

    if not bool(options):
        utils.print_description(COMMAND_NAME, AVAILABLE_OPTIONS)

    functions.close_connection(conn)
    return



def register_options():
    options = {}
    iterable_args = iter(sys.argv[2:])
    for arg in iterable_args:
        if utils.is_option(arg):
            if arg.lower() in AVAILABLE_OPTIONS:
                if AVAILABLE_OPTIONS[arg]['arg_required']:
                    options[arg.lower()] = next(iterable_args)
                else:
                    options[arg.lower()] = True
            else:
                utils.print_unknown_option(arg)
                return

    return options


def main():
    global COMMAND_NAME
    COMMAND_NAME = sys.argv[1]

    options = register_options()
    execute_cmd(options)


if __name__ == '__main__':
    main()
    exit()
