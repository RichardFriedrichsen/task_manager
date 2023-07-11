#=====importing libraries===========
import datetime
from datetime import date 
import math
import re
import json
import os
import time

#====Login Section====
# Defining Variables
current_user = ""
user_logged_in_status = False

password_list = []
task_file = "tasks.txt"
user_file = "user.txt"
report_file_tasks = "task_overview.txt"
report_file_users = "user_overview.txt"
date_format = "%d/%m/%Y"
today = datetime.date.today().strftime("%d/%m/%Y")

def get_users_passwords():
    ''' Creates a list of usernames and passwords writes them to a file

        returns a list of username and passwords
    '''

    user_pw_list = []
    user_list = []
    password_list = []
    # Adding usernames and password to a list from user file
    user_file = open("user.txt", "r")
    for line in user_file:
        user_pw_list += line.split(',')
    user_pw_list = [str.strip() for str in user_pw_list] # removing \n
    user_file.close()
    
    # Iterating through username and password list backwards. Popping off every odd item, which is the pw, then reversing the list.
    user_list = user_pw_list
    for i in range(len(user_pw_list),0,-1):
        if i % 2 != 0:
            password_list.append(user_pw_list[i])
            user_list.pop(i)
    password_list.reverse()

    return password_list, user_list

#==== Functions ====#
def date_validation(date_string):
    ''' Validates a date string

        Args: 
        date_string (str): date string with format dd/mm/yyyy

        returns:
        Boolean
    '''
    try:
        datetime.datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def read_file(file_to_open):
    ''' Reads file and saves contents

        Args:
        file_to_open (str): file path to file 
    '''
    file = open(file_to_open,"r")
    file_contents = file.read()
    file.close()
    return file_contents

def write_file(file_to_write, option, content):
    ''' Writes contents to a file

        Args:
        file_to_write (str): file location of file to write to
        options (str): argument of to which type of writing should be done i.e "w" or "a"
        content (any): Can be any content
    '''
    task_file = open(file_to_write, option)
    task_file.write(content)
    print("\nSuccessfully written to file!")
    task_file.close()

def write_mod_task(file_to_write, option,content):
    '''Writes contents to a file

        Args:
        file_to_write (str): file location of file to write to
        options (str): argument of to which type of writing should be done i.e "w" or "a"
        content (any): Can be any content
    '''
    task_file = open(file_to_write, option)
    task_file.write(content)
    task_file.close()

def reg_user():
    '''Gets user input for password and username, checks if username exists, if not saves password and username to file


    '''
    password_list, user_list = get_users_passwords()
    print("\nTo create a new user:\n")
    new_username = input("Please enter a username: ")
    new_password = input("Please enter a your password: ")
    new_password2 = input("Please confirm your password: ")

    # Checking if passwords are the same and if username is unique
    if new_password == new_password2 and new_username not in user_list:
        user_txt = open(user_file, 'a')
        user_txt.write("\n" + new_username + ", " + new_password)
        print("\nUser successfully created!\n")
        user_txt.close()
    
    elif new_password != new_password2:
        try_again = input("Passwords do not match. 'Y' to try again. \n").lower()
        if try_again == "y":
            reg_user()
    else:
        try_again = input("\nUsername already taken. 'Y' to try again.\n").lower()
        if try_again == "y":    
            reg_user()

# reading file, returns 0 if empty or list of dictionaries
def get_all_tasks():
   
    # Reading the file
    file_contents = read_file(task_file)
    file_contents = file_contents.replace("'", "\"")
    file_contents = file_contents.split("\n")

    # Checking if there are content, otherwise json loads will return an error
    if len(file_contents) < 2:
        return 0
    
    # Looping over file and adding tasks as dictionary to array
    else:
        dict_arr = []
        for item_num in range(0,len(file_contents)-1):
            dict_arr.append(json.loads(file_contents[item_num]))
        return dict_arr

# gets array of all tasks as dictionary, gets input and writes to file as dictionary
def add_task():
    dict_array = get_all_tasks()

# If dictionary is empty assigning task_number one, otherwise len(dictionary)
    if isinstance(dict_array,int):  
       
        task_number = 0 # If dictionary is empty, then task number is 1
        task_title = input("What is the title of the task: ")
        task_assigned_to = input("Who do you want to assign the Task to: ").lower()
        task_description = input("Please enter a description: ")
        task_due_date = input("Please enter the due date format(dd/mm/yyy) for the task: ")
        task_created = datetime.date.today().strftime("%d/%m/%Y")
        task_is_complete = input("Has the task been completed: ").lower() or "no"
    elif len(dict_array) > 0:
        task_number = len(dict_array)
        task_title = input("What is the title of the task: ")
        task_assigned_to = input("Who do you want to assign the Task to: ").lower()
        task_description = input("Please enter a description: ")
        task_due_date = input("Please enter the due date format(dd/mm/yyy) for the task: ")
        task_created = datetime.date.today().strftime("%d/%m/%Y")
        task_is_complete = input("Has the task been completed: ").lower() or "no"

    if date_validation(task_due_date):
        task = {}
        task.update({
            "task": task_number,
            "assignee":task_assigned_to,
            "title":task_title,
            "created_by": current_user,
            "description": task_description,
            "due_date": task_due_date,
            "created_date": task_created,
            "completed": task_is_complete
        })
        
    else: 
        print("\nNo valid date provided, please try again.\n")
        return
    
    # # Creating a task in txt file
    write_file(task_file,"a", str(task)+"\n")

# Gets all tasks and prints them to console
def view_all():
    # Getting all tasks
    dict_array = get_all_tasks()
    
    if dict_array == 0:
        print("\n"+"-" * 60)
        print("No Tasks to show")
        print("\n"+"-" * 60)
    else:
        # Printing Tasks in output 2 format
        for dict in dict_array:
            print("-" * 60)
            print(f"Task no: \t\t{dict['task']+1}")
            print(f"Task name: \t\t{dict['title']}")
            print(f"Assigned to: \t\t{dict['assignee']}")
            print(f"Date Assigned: \t\t{dict['created_date']}")
            print(f"Due Date: \t\t{dict['due_date']}")
            print(f"Task complete:\t\t{dict['completed']}")
            print(f"Task description:\n{dict['description']}")

# Gets logged in users tasks and prints them to console
def view_mine():
     # Reading the file
    dict_array = get_all_tasks()
    my_tasks = []

    for dict in dict_array:
        if dict["assignee"] == current_user:
            my_tasks.append(dict)

    if len(my_tasks) == 0:
        print("\n"+"-" * 60)
        print(f"\nNo Tasks to show for {current_user}")
        print("\n"+"-" * 60)
    else:
        # Printing out tasks for current user
        for dictionary in my_tasks:
            print("-" * 60)
            print(f"Task: \t\t\t{dictionary['task']+1}")
            print(f"Task name: \t\t{dictionary['title']}")
            print(f"Assigned to: \t\t{dictionary['assignee']}")
            print(f"Date Assigned: \t\t{dictionary['created_date']}")
            print(f"Due Date: \t\t{dictionary['due_date']}")
            print(f"Task complete:\t\t{dictionary['completed']}")
            print(f"Task description:\n{dictionary['description']}")

# Logic to modify task after selecting view_mine
def modify_task():
    dict_array = get_all_tasks()
    new_dictionary = ""

    task_number = int(input("\nTo modify please enter the number of task. '-1' to return to main menu: \n"))
    if task_number == -1:
        return
    else:
        option = int(input(f"\nTask {task_number} selected.\nPlease select '1' to edit the task or '2' to mark it as complete, 'e' to exit:\n"))
        
        if option == 2:
            print(f"Task number: {dict_array[task_number]['task']} marked as complete!")
            dict_array[task_number-1]['completed'] = "yes"
            
            for item in dict_array:
                new_dictionary += str(item) + "\n"
            write_mod_task(task_file,'w',new_dictionary)
        
        elif option == 1:
            if dict_array[task_number-1]['completed'] != "yes":
                task_assigned_to = input("Who do you want to assign the Task to: ").lower()
                task_due_date = input("Please enter the due date format(dd/mm/yyy) for the task: ")

                dict_array[task_number-1]['assignee'] = task_assigned_to
                dict_array[task_number-1]['due_date'] = task_due_date

                for item in dict_array:
                    new_dictionary += str(item) + "\n"
                write_mod_task(task_file,'w',new_dictionary)
            else: 
                print(f"Task already completed.")
        elif option == 'e':
            return

# Gets a list of all tasks, generates a string of task statistics and writes them to file
def generate_report_tasks():

    dict_task_list = get_all_tasks() 

    # Checking if there are any tasks
    if dict_task_list == 0:
        print("-"*60)
        print("\nNo tasks, cannot generate report.\n")
        print("-"*60)

    else:
        total_num_tasks = len(dict_task_list)
        total_num_complete = 0
        total_num_uncomplete = 0
        total_num_uncomplete_overdue = 0

        # Iterating through each dictionary and adding to running total based on criteria       
        for task in dict_task_list:
            if task["completed"] == "yes":
                total_num_complete += 1

            if task["completed"] == "no":
                total_num_uncomplete += 1

            if task["completed"] == "no" and datetime.datetime.strptime(task["due_date"], date_format).date() > datetime.datetime.strptime(today, date_format).date():
                total_num_uncomplete_overdue += 1
        
        percentage_incomplete = round(total_num_uncomplete/total_num_tasks * 100,2)
        percentage_overdue = round(total_num_uncomplete_overdue / total_num_tasks * 100,2)

        task_report_str = "-"*60 + f'''
The report has been generated for {today}:

Total number of Tasks:\t\t\t\t\t{total_num_tasks}
Total number completed:\t\t\t\t\t{total_num_complete}
Total number of not completed and overdue:\t{total_num_uncomplete_overdue}
Percentage of incomplete tasks:\t\t\t{percentage_incomplete}%
Percentage of overdue tasks:\t\t\t\t{percentage_overdue} %''' + "\n" + "\n" + "-"*60

        write_file(report_file_tasks,"w",task_report_str)





    users = []
    total_num_users = 0
    total_num_tasks = 0

# ▪ For each user also describe:
    total_tasks_user = 0
    total_task_completed_user = 0 # percentage
    total_tasks_outstanding = 0 # percentage
    tasks_outstanding_overdue = 0 # percentage
    
    for user in users:
        print("test")

# Gets a list of users and tasks, generates a string of statistics for each user and writes them to file
def generate_report_users():
    password_list, user_list = get_users_passwords()
    dict_task_list = get_all_tasks() 
    total_num_tasks = len(dict_task_list)

# Creating a dictionary of user stats:
    user_stats = {}
    for user in user_list:
        user_stats[user.lower()] = {
            "total_tasks" : 0,
            "total_tasks_completed" : 0,
            "total_tasks_not_complete": 0,
            "total_task_not_c_overdue": 0,
        }

    # Incrementing over dictionaries if different tasks options apply
    for user in user_list: 
        user = user.lower()
        for task in dict_task_list:
            if task["assignee"].lower() == user:
                user_stats[user]["total_tasks"] += 1

                if task["completed"] == "yes":
                    user_stats[user]["total_tasks_completed"] += 1

                elif task["completed"] == "no":
                    user_stats[user]["total_tasks_not_complete"] += 1
                    if datetime.datetime.strptime(task["due_date"], date_format).date() < datetime.datetime.strptime(today, date_format).date():
                        user_stats[user]["total_task_not_c_overdue"] += 1
           
    
    stats_string = "-"*60 +"\n" + f"Total number of users: {len(user_list)}\n" + f"Total number of Tasks: {len(dict_task_list)}\n"
    for key in user_stats:
        stats_string += "\n"
        stats_string += f"User: \t\t\t\t{key.title()}\n"
        stats_string += f"Total tasks:\t\t\t{user_stats[key]['total_tasks']}\n"
        stats_string += f"Total assigned to {key}:  \t{round(user_stats[key]['total_tasks']/total_num_tasks*100,2)}%\n"
        stats_string += f"Tasks completed:  \t\t{round(user_stats[key]['total_tasks_completed']/total_num_tasks*100,2)}%\n"
        stats_string += f"Still to be completed:\t\t{round(user_stats[key]['total_tasks_not_complete']/total_num_tasks*100,2)}%\n"
        stats_string += f"Uncomplete and overdue:\t\t{round(user_stats[key]['total_task_not_c_overdue']/total_num_tasks*100,2)}%\n"
    stats_string += "-"*60
    
    write_file(report_file_users,"w",stats_string)

# Checks if the tasks and user reports have been created if not runs them, prints results to console
def user_statistics():
    if os.path.exists(report_file_tasks):
        task_file_contents = read_file(report_file_tasks)
    else:
        generate_report_tasks()
        time.sleep(2)
        task_file_contents = read_file(report_file_tasks)

    if os.path.exists(report_file_users):
        user_file_contents = read_file(report_file_users)
    else:
        generate_report_users()
        time.sleep(2)
        user_file_contents = read_file(report_file_users)
    print(task_file_contents)
    print(user_file_contents)

# Gets a list of passwords and usernames, checks user input credentials and loggs the user in 
def logging_in ():
    user_logged_in_status = False
    password_list, user_list = get_users_passwords()
    global current_user
    # User authentication section
    while not user_logged_in_status:

        # Getting user input
        print("\nWelcome to the Task creator, to login:\n")
        in_username = input("Please enter your username: ")
        in_password = input("Please enter your password: ")
        pwd_index = 0

        # Checking if user is in user list, name is case sensitive
        if in_username in user_list:
            pwd_index = user_list.index(in_username)

            # Checking if password with same index as username is true
            if in_password == password_list[pwd_index]:
                user_logged_in_status = True
                print(f"\nHey {in_username}, you have successfully logged in!")
                current_user = in_username.lower()
            else:
                print("\nSorry your password is wrong. Please try again. \n")
        else:
            print("No user found.")

# Start of app: calling loggin in function
logging_in()

# Logic: Creates the flow of the application based on user input
while True:

    if current_user == "admin":
        menu = input('''Select one of the following Options below:

r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
    else: 
        menu = input('''

Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()
    



    # Creating a new user
    if menu == 'r' and current_user == "admin":
        pass
        reg_user()

    # Adding a new task
    elif menu == 'a':
        pass
        add_task()
        
    # Reading and outputting task file to console
    elif menu == 'va':
        pass
        view_all()

    elif menu == 'vm':
        pass
        view_mine()
        modify_task()
    
    # Statistics
    elif menu == 'ds':
        user_statistics()
        
    
    elif menu == 'gr':
        generate_report_tasks()
        generate_report_users()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")


