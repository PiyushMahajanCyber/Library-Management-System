import mysql.connector as my
from tabulate import tabulate as tab
from datetime import date, timedelta

con = my.connect(host="localhost", user="root", password="Piyush2006", database="library_management_system")
cur = con.cursor()

# ---------------- DISPLAY FUNCTIONS ----------------
def show():
    cur.execute("SELECT * FROM Books")
    data = cur.fetchall()
    headers = [c[0] for c in cur.description]
    print(tab(data, headers, tablefmt="grid"))

def show_records():
    cur.execute("SELECT * FROM Records")
    data = cur.fetchall()
    headers = [c[0] for c in cur.description]
    print(tab(data, headers, tablefmt="grid"))

def show_users():
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    headers = [c[0] for c in cur.description]
    print(tab(data, headers, tablefmt="grid"))

# ---------------- BOOK MANAGEMENT ----------------
def insert():
    try:
        Book_ID = int(input("Enter Book_ID:"))
        Title = input("Enter Title:")
        Author = input("Enter Author:")
        cur.execute("INSERT INTO Books VALUES(%s,%s,%s)", (Book_ID, Title, Author))
        con.commit()
    except:
        print("Invalid input or duplicate Book_ID")

def delete():
    Book_ID = int(input("Enter Book_ID to delete:"))
    cur.execute("DELETE FROM Books WHERE Book_ID=%s", (Book_ID,))
    con.commit()

def update():
    print("1.Title  2.Author  3.Genre  4.Stock  5.Back")
    choice = int(input("Choice:"))
    if choice == 5:
        return

    Book_ID = int(input("Enter Book_ID:"))
    field_map = {1: "Title", 2: "Author", 3: "Genre", 4: "Stock"}
    if choice in field_map:
        new_val = input("Enter new value:")
        cur.execute(f"UPDATE Books SET {field_map[choice]}=%s WHERE Book_ID=%s", (new_val, Book_ID))
        con.commit()
    else:
        print("Invalid choice")

# ---------------- ISSUE BOOK ----------------
def Issue(User_ID):
    Book_ID = int(input("Enter Book_ID to issue:"))

    # Check stock
    cur.execute("SELECT Stock FROM Books WHERE Book_ID=%s", (Book_ID,))
    stock = cur.fetchone()
    if not stock:
        print("Book does not exist")
        return
    if stock[0] <= 0:
        print("Book out of stock")
        return

    # Prevent duplicate issue
    cur.execute("SELECT * FROM Records WHERE Book_ID=%s AND User_ID=%s AND Return_Date IS NULL", (Book_ID, User_ID))
    if cur.fetchone():
        print("You already issued this book")
        return

    today = date.today()
    due_date = today + timedelta(days=10)

    cur.execute("INSERT INTO Records(Book_ID,User_ID,Issue_Date,Due_Date) VALUES(%s,%s,%s,%s)", (Book_ID, User_ID, today, due_date))
    cur.execute("UPDATE Books SET Stock=Stock-1 WHERE Book_ID=%s", (Book_ID,))
    con.commit()
    print("Book issued successfully")

# ---------------- RETURN BOOK ----------------
def Return(User_ID):
    Book_ID = int(input("Enter Book_ID to return:"))

    cur.execute("SELECT Due_Date FROM Records WHERE Book_ID=%s AND User_ID=%s AND Return_Date IS NULL", (Book_ID, User_ID))
    result = cur.fetchone()

    if not result:
        print("No active issue record found")
        return

    due_date = result[0]
    return_date = date.today()
    delay_days = (return_date - due_date).days

    fine = delay_days * 10 if delay_days > 0 else 0
    if fine:
        print(f"Fine: Rs.{fine}")

    cur.execute("UPDATE Records SET Return_Date=%s WHERE Book_ID=%s AND User_ID=%s AND Return_Date IS NULL", (return_date, Book_ID, User_ID))
    cur.execute("UPDATE Books SET Stock=Stock+1 WHERE Book_ID=%s", (Book_ID,))
    con.commit()
    print("Book returned successfully")

# ---------------- MENUS ----------------
def Admin():
    while True:
        print("\n*** ADMIN ***")
        print("1.Insert 2.Delete 3.Update 4.Show Books 5.Show Records 6.Show Users 7.Exit")
        choice = int(input("Choice:"))
        if choice == 1: insert()
        elif choice == 2: delete()
        elif choice == 3: update()
        elif choice == 4: show()
        elif choice == 5: show_records()
        elif choice == 6: show_users()
        elif choice == 7: break
        else: print("Invalid choice")

def Student(User_ID):
    while True:
        print("\n*** STUDENT ***")
        print("1.Available Books 2.Issue 3.Return 4.Exit")
        choice = int(input("Choice:"))
        if choice == 1: show()
        elif choice == 2: Issue(User_ID)
        elif choice == 3: Return(User_ID)
        elif choice == 4: break
        else: print("Invalid choice")

# ---------------- LOGIN ----------------
User_ID = input("Enter User_ID:")
Pass = input("Enter Password:")

cur.execute("SELECT * FROM users WHERE User_ID=%s AND Password=%s", (User_ID, Pass))
row = cur.fetchone()

if row:
    if row[2] == "Admin":
        Admin()
    else:
        Student(User_ID)
else:
    print("Invalid credentials")