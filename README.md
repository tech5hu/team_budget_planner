# Team Budget Planner Web Application
## Overview
This web application helps teams manage and track budgets and transactions with user roles and permissions. It supports different account levels and roles, allowing Managers to have admin access and Developers to be regular users. The system keeps track of teams, budgets, transactions, and expense categories. Admin users have the ability to fully manage budgets and transactions, while regular users can only create, view, and update relevant data.

# Installation
## Local Installation - Install the following on your machine:
### Prerequisites
- **Python 3.x**
   Python is a programming language used to build the application. Follow the instructions here to download and install Python for your device: (https://www.python.org/downloads/)

    After installation, verify that it was successful by running the following command in your terminal or command prompt:

     
     python3 --version

This command will display the installed Python version.
        

- **Git**
   Git is a version control system that allows you to track changes in your code and collaborate with others. Follow the instructions here to install Git for your device: (https://git-scm.com/downloads)

    After installation, verify that it was successful by running:

     
     git --version


- **PostgreSQL**
   PostgreSQL is a powerful relational database system used to store the application’s data. Follow the instructions here to install PostgreSQL for your device: (https://www.postgresql.org/download/)

   if you have Homebrew installed you can run (can take up to 10 mins)

     
     brew install postgresql@15

   After installation, verify that it was successful by running:
     
     
     psql --version

**Installation Steps**

**Clone the repository**
  This step downloads the application code from GitHub to your local machine. Run the following commands in your terminal:

   
    git clone https://github.com/tech5hu/team_budget_planner
    
    cd team_budget_planner


**Create and activate a virtual environment**
  This isolates your project dependencies. Run the following commands:

   
   python3 -m venv env

   
   source env/bin/activate  # On Windows: env\Scripts\activate

**Install the dependencies**
  This step installs all the necessary packages required for the application to run (can take up to 10 mins). Run:

   
   pip install -r requirements.txt

**Set up the database using PostgreSQL**
  Ensure you have downloaded PostgreSQL as instructed above:

  To set up the database, start PostgreSQL and create a user and database by running the following commands in your terminal:

        
        psql postgres

  Then, within the PostgreSQL shell, run these commands:

   -- Important: Before executing the commands below, please make sure to replace your_db_user, your_password, and your_db_name with your own desired values. Failure to do so may result in unintended database and user creation. 

   -- *Example: Creating a user*
   -- *Example: *CREATE USER team_user WITH PASSWORD 'secure_password123';*

   -- Create a new database to be used in your application and set the previously created user as the owner, replace your_db_name with your desired database name.

      -- *Example: Creating a database*
      -- *Example: CREATE DATABASE team_budget OWNER team_user;*

   -- For reference:
         
         CREATE USER your_db_user WITH PASSWORD 'your_password';
         
         CREATE DATABASE your_db_name OWNER your_db_user;


   **If you accidentally created a database or user and wish to remove them, follow these steps:**
         
         DROP DATABASE your_db_name;
         
         DROP USER your_db_user;


  Once user and database created quit PostgreSQL by running: 

      
       \q



**Update the .env file**
 Create a .env file in the project root with the following variables:
     
     SECRET_KEY=your-secret-key
     DEBUG=True
     DATABASE_URL=postgres://your_db_user:your_password@localhost:5432/your_db_name

   (You can generate a SECRET_KEY using the following command:)

     
     python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'


**Apply Database Migrations**
 Finally apply Database Migrations:

   Run the following command in your terminal to apply the database migrations and set up the initial database schema to be used in the app:
     
     python3 manage.py migrate
 

**Run the development server:**
This command starts a local server that allows you to view the application in your web browser:

python3 manage.py runserver

**Access the app:**
Once the server is running, open your web browser and navigate to:

http://127.0.0.1:8000  ----> web application

http://127.0.0.1:8000/admin/  -----> django admin site (for database management)

You can now log in or register as a new user and start using the app!

**Admin Credentials**

     Username: 'admin'
     Password '123'


**HOSTED LIVE VERSION (Heroku)**
You can access the live version of the application hosted on Heroku here: 

      https://teambudgetplanner-fd1be9ca9c90.herokuapp.com/


Open the Heroku URL: Navigate to the live application using the link provided above.

Register an account: If you are a new user, follow the registration process. If you already have an account, log in using your credentials.


**App Navigation Key**

User Roles: Depending on your role (Manager or Developer):

Managers can create, view, update, and delete budgets and transactions.
Developers can create, view, and update budgets and transactions, but cannot delete them.
Dashboard: Use the dashboard to view summary information about budgets, transactions, and expense categories.

Budget Page: View a list of all budgets, including further details, and create, update, or delete them (based on permissions).

Transaction Page: View a list of all transactions, including further details, and create, update, or delete them (based on permissions).

User Profile Page: View your username, email, account level, team, and work phone number.

Settings Page: Change your password and update your notification settings.

Recent Budgets Sidebar: View all recent budgets.

Add Transaction Sidebar: Add a new transaction.

Generate Report Sidebar: Generate a spending report by transaction expense category and view all transactions in a table.

Log In and Log Out Pages: Use these pages to log in and out of the application, reset forgotten passwords, or register a new account.
