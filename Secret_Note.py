import datetime
from os import path
from os import listdir
from os import mkdir
from os import remove
import shutil

db_path = './DataBase/'
password_file = db_path+"passwordInfo.txt"

menu ='''
    1. Register to Secret Note
    2. Login to Secret Note
    3. Retrieve Password
    4. Exit
    What do you want to do: '''
    
menu1 = '''
What do you want to do :
    1. Keep a secret
    2. View old secrets
    3. Delete a secret
    4. Delete profile
    5. Logout
'''

menu2 ='''
secret exists with same title.
    1. Do you want to add more to the same secret.
    2. Do you want to re-write the secret.
    Press other key to Cancel.
'''

def check_in_file(filename, username, password='', mode=''):
    with open(filename, 'rt') as fd:
        for line in fd:
            line = line.split('\n')[0].split(',')
            if mode == 'password' and line == [username,password]:
                return True
            if mode == 'user' and line[0] == username:
                return True
            if mode == 'retrieve' and line[0] == username:
                print('Your password : ',line[1])
                return True
        else:
            return False

def password_check(username):
    password = input("Password: ")
    check_status = check_in_file(password_file, username, password, mode='password')
    return check_status

def create_dic(user):
    user = user.strip()
    if user != "":
        dir_path = './DataBase/'+user
        mkdir(dir_path)
        return True
    else:
        return False

def fileWrite(data, filename, mode):
    with open(filename, mode) as fd:
        fd.write(data+'\n')

def new_password(username):
    Password = input('Create New Password : ').strip()
    try_count = 3
    while Password == "" and try_count > 0:
        Password = input("Password should contain something. Try again : ").strip()
        try_count -= 1
    if try_count == 0 and Password == "":
        return False
    else:
        data = username+','+Password+'\n'
        fileWrite(data, password_file, 'a')
        return True

def create_user(user, user_list=[]):
    user = user.strip()
    if user_list:
        if (not user) or (user in user_list):
            user = input("username already used. Try another username: ").strip().upper()
            user, _ = create_user(user, user_list)
    else:
        if not user :
            user = input("invalid. Try another username: ").strip().upper()
            user, _ = create_user(user, user_list)
    return (user,True)

def select_user_or_create():
    verified_user = False
    user = ''
    login_check = input(menu)
    if login_check == '1':
        print("\n====Register===")
        try:
            user_list = [d for d in listdir(db_path) if path.isdir(path.join(db_path, d))]
        except Exception:
            mkdir(db_path)
            user_list = [d for d in listdir(db_path) if path.isdir(path.join(db_path, d))]
        user = input("Enter username: ").strip().upper()
        user, flag = create_user(user, user_list)
        if flag:
            verified_user = new_password(user)
            if not verified_user:
                    print('Invalid password')
                    verified_user, user = select_user_or_create()
            else:
                print(f'''
        ==Welcome {user} to Secret Note==\n
        ''')
    elif login_check == '2':
        print("\n====Login===")
        user = input("Enter username: ").strip().upper()
        if path.exists(password_file) and user != "":
            if check_in_file(password_file, user, mode = 'user'):
                verified_user = password_check(user)
                if not verified_user:
                    print('Invalid password')
                    verified_user, user = select_user_or_create()
                else:
                    print(f'''
        ==Welcome Back {user}==\n
        ''')
            else:
                print('Invalid username')
                verified_user, user = select_user_or_create()
        else:
            print('Invalid username')
            verified_user, user = select_user_or_create()
    elif login_check == '3':
        print("\n====Retrieve password===")
        user = input("Enter username: ").strip().upper()
        if path.exists(password_file) and user != "":
            if not check_in_file(password_file, user, mode='retrieve'):
                print('username not found\n')
        else:
            print("Username not found\n")
        retrieve_flag = input('Do you want to exit?\n press n/no to continue \n Any other key to exit(No):').strip().lower()
        if retrieve_flag in n_flags:
            verified_user, user = select_user_or_create()
    elif login_check == '4':
        print('Comeback again')
    else:
        print('Invalid input')
        verified_user, user = select_user_or_create()

    return (verified_user,user)

def keep_secrets(user):
    while(True):
        filename = input('Title : ').strip()
        if filename == "":
            print("Title should content some characters. Try again")
            filename = input('Title : ').strip()
        if filename != "":
            filepath = './DataBase/'+user+'/'+filename+'.txt'
            if path.exists(filepath):
                note_choice = input(menu2+'Enter your choice : ')
                if(note_choice == '1'):
                    note = input('Note : ')
                    fileWrite(note, filepath, 'a')
                    print('Your secret is saved successfully\n')

                elif note_choice == '2':
                    note = input('Note : ')
                    fileWrite(note, filepath, 'w')
                    print('Your secret is saved successfully\n')
                else:
                    print("Canceled successfully.")
            else:
                note = input('Note : ')
                fileWrite(note, filepath, 'w')
                print('Your secret is saved successfully\n')
        else:
            print("Invalid Title")
            break
        cont_flag = input('Do you want to keep another secret?(no)').lower()
        if cont_flag in n_flags:
            break
        elif cont_flag not in y_flags:
            print('Invalid parameter')
            break

def show_sectets(user):
    file_list = [d for d in listdir(db_path + user)]
    if len(file_list) != 0:
        print('=================Your secrets===================')
        for notes in file_list:
            print(notes.split('.')[0])
        print('=================================================')

        open_secret = input('Do you want to open any secret:(no):').lower()
        if open_secret in y_flags:
            secret_name = input('Enter the secret name: ')
            try:
                with open(db_path + user + '/' + secret_name + '.txt') as fd:
                    print('\n<**> Here is your secrect about \"'+secret_name+'\"<**> \n')
                    print(fd.read())
            except Exception:
                print("This secrect is not shared with me")
        elif open_secret not in n_flags:
            print('Invalid parameter')
    else:
        print("No secrets found")

def delete_secret(user):
    file_list = [d for d in listdir(db_path + user)]
    if len(file_list) != 0:
        print('=================Your secrets===================')
        for notes in file_list:
            print(notes.split('.')[0])
        print('=================================================')
        secret_to_delete = input('Which Secret do you want to delete : ')
        if path.exists(db_path + user + '/' + secret_to_delete + '.txt'):
            delete_confermation = input("Do you really want to delete (No) : ").lower()
            if delete_confermation in y_flags:
                remove(db_path + user + '/' + secret_to_delete + '.txt')
            elif delete_confermation not in n_flags:
                print("Invalid parameter\nBut Your Secret is safe with me\n")
        else:
            print("This secret is not shared with me")
    else:
        print("No secrets found")

def delete_profile(user):
    profile_flag = input('Do you really want to delete the profile(No):').lower()
    if profile_flag in y_flags:
        shutil.rmtree(db_path + user)
        with open(password_file ,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if user not in line:
                    f.write(line)
            f.truncate()
        return True
    elif profile_flag not in n_flags:
        print('Invalid input')
    return False

def run():
    verified_user, username = select_user_or_create()
    if verified_user:
        try:
            create_dic(username)
        except Exception:
            pass
        while(True):
            user_choice = input(menu1+'Your choice : ')
            if user_choice == '1':
                keep_secrets(username)
            elif user_choice == '2':
                show_sectets(username)
            elif user_choice == '3':
                delete_secret(username)
            elif user_choice == '4':
                if delete_profile(username):
                    print('Profile deleted successfully')
                    break
            elif user_choice == '5':
                logout_flag = input("Do you really want to log out (no):").strip().lower()
                if logout_flag in y_flags:
                    print('**See you next time**')
                    run()
                    break
                elif logout_flag not in n_flags:
                    print('Invalid parameter')
            else:
                print('Invalid input')
    return

if __name__ == "__main__":
    y_flags = ['y','yes']
    n_flags = ['n','no','']
    run()
