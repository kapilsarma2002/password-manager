import mysql.connector as mysql
from tabulate import tabulate
import random
import string
import pwinput

database_name = "mydatabase"
table_name = "userinfo"

while True:
    try : 
        db = mysql.connect(
            host = "localhost",
            user = "root",
            # passwd = getpass.getpass("Enter the root password : "),
            passwd = pwinput.pwinput(prompt = "Enter root password : ", mask = '*'),
            database = database_name,
            buffered = True
        )
        break
    except :
        print('Wrong password! Try again!')


# display menu
def menu():
    print("---------------------------------------")
    print("0. For viewing all the saved info")
    print("1. For adding the user info ")
    print("2. For updating the info ")
    print("3. For deleting the info")
    print("-1. Exit")
    print("---------------------------------------")


# generates a random password
def generate_password(digit):
    password = ""
    for _ in range(digit):
        char = random.choice(string.ascii_letters)
        password += char
    return password


# insert user information
def insert_info(userid):
    cursor = db.cursor()
    #username
    username = input("Enter your username : ")
    #email
    email = input("Enter the email for the account : ")
    #website
    website = input("Enter the name of the Website : ")
    #url
    url = input("Enter the url of the website : ")    
    #password
    password = ''
    i = int(input("Select\n 1 : if you want to create the password\n 2 : if you want to generate new password : "))
    if i==1:
        password = pwinput.pwinput(prompt = "Enter your password : ", mask = '*')
    elif i==2:
        #generate random password
        digit = int(input("Enter how many digit password you want : "))
        password = generate_password(digit)
    else:
        print("Enter a valid key!")
        return
    t = (userid,username,email,website,url,password)
    insert = "INSERT INTO " + table_name + " VALUES(%s, %s, %s, %s, %s, %s);"
    cursor.execute(insert,t)
    db.commit()
    print("\nTable updated!")


# update user information
def update_info(userid):
    user = input("Enter the username to update : ")
    website = input("Enter the website to update : ")
    cursor = db.cursor()
    search = "SELECT userid,username,website FROM " + table_name
    cursor.execute(search)
    data = cursor.fetchall()
    # print(data)
    if (userid,user,website) not in data :
        print("Enter a valid argument!")
        return
    
    new_password = ''
    i = int(input("Select\n 1 : if you want to create the password\n 2 : if you want to generate new password : "))
    if i==1:
        new_password = pwinput.pwinput(prompt = "Enter your password : ", mask = '*')
    elif i==2:
        #generate random password
        digit = int(input("Enter how many digit password you want : "))
        new_password = generate_password(digit)
    else:
        print("Enter a valid key!")
        return

    t = (new_password,userid,user,website)
    update = "UPDATE " + table_name + " SET password = %s WHERE userid = %s AND username = %s AND website = %s"
    cursor.execute(update,t)
    db.commit()
    print("\nTable updated!")


# delete user information
def delete_info():
    user = input("Enter the username to delete : ")
    website = input("Enter the website to delete : ")
    cursor = db.cursor()
    search = "SELECT username,website FROM " + table_name
    cursor.execute(search)
    data = cursor.fetchall()
    # print(data)
    if (user,website) not in data :
        print("Enter a valid argument!")
        return
    
    t = (user,website)
    update = "DELETE FROM " + table_name + " WHERE username = %s AND website = %s"
    cursor.execute(update,t)
    db.commit()
    print("\nTable updated!")


# print all the saved info so far
def print_table(userid):
    cursor = db.cursor()
    query = "SELECT * FROM " + table_name + " WHERE userid = %s"    
    t = (userid,)
    cursor.execute(query,t)
    print(tabulate(cursor,headers=["userid","username","email","website","url","password"], tablefmt="psql"))


#manage
def manage(userid):
    while True:
        menu()
        key = int(input("Enter the key of the operation you want to perform : "))
        if key==-1: 
            print("Thanks for using the program")
            exit()
        if key==1 : insert_info(userid)        
        elif key==2 : update_info(userid)
        elif key==3 : delete_info()
        elif key==0 : print_table(userid)


#adding new user
def add_new_user():
    print("Adding user...")
    cursor = db.cursor()
    size = "SELECT COUNT(userid) FROM USERS"
    cursor.execute(size)
    n = cursor.fetchone()
    pid = n[0]+1
    username = input("Enter username : ")
    password = pwinput.pwinput(prompt = "Enter your password : ", mask = '*')
    t = (pid,username,password)
    add = "INSERT INTO USERS VALUES (%s,%s,%s);"
    cursor.execute(add,t)
    print('User added!')
    db.commit()
    manage(pid)


#checking user
def check_user():
    print("Checking user...")
    found = False
    p = ''
    cursor = db.cursor()
    user_name = input("Enter username : ")    
    search = "SELECT username,password FROM USERS;"
    cursor.execute(search)
    data = cursor.fetchall()
    # print(data)
    for i in data:
        # print(i[0], i[1])
        if i[0] == user_name:
            found = True
            p = i[1]
            break

    if found:
        password = pwinput.pwinput(prompt = "Enter your password : ", mask = '*')
        if p==password :
                get_id = "SELECT userid from USERS WHERE username = %s"
                d = (user_name,)
                cursor.execute(get_id,d)
                id = cursor.fetchone()
                # print(id[0])
                manage(id[0])
        else :
            print('Wrong password!')
            exit()
    else :
            print("User does not exist!")
            add_new_user()   


if __name__ == "__main__":
    check_user()

# closes the database connection
db.close()