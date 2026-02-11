# Library Management System
A role-based Library Management System built using Python and MySQL, designed to automate book inventory, issuing, returning, and fine calculation.


# Features
•	🔐 User authentication (Admin / Student)
•	📖 Book inventory management
•	🔄 Issue & return tracking
•	📅 Due date calculation
•	💰 Automatic fine calculation for late returns
•	📊 Records & user database view
•	📦 Stock auto-updated on issue/return


# System Design
The system follows a modular architecture:

Module	Responsibility
Book Management	Add, update, delete books
User Management	Store user credentials & roles
Issue/Return	Track transactions & update stock
Fine System	Calculates delay using date difference

Database uses relational design with referential integrity.


# Tech Stack
•	Python
•	MySQL
•	mysql-connector-python
•	tabulate


# Database Tables

Books
	•	Book_ID (PK)
	•	Title
	•	Author
	•	Genre
	•	Stock

Users
	•	User_ID (PK)
	•	Password
	•	Role (Admin/Student)

Records
	•	Book_ID (FK)
	•	User_ID (FK)
	•	Issue_Date
	•	Due_Date
	•	Return_Date


# How to Run
	
  1.	Install dependencies:

pip install mysql-connector-python tabulate

	2.	Create MySQL database and tables
	3.	Update DB credentials inside the program
	4.	Run:

Library_Management_System.py


# Future Improvements
•	Search by title/author
•	Overdue report generation
•	GUI version
•	Password hashing
•	Web deployment

# Author

Developed as a database-backed application demonstrating real-world inventory and transaction logic.
