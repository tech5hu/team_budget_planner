# Team Budget Planner Web Application

## Overview

This web application helps teams manage and track budgets and transactions with user roles and permissions. It supports different account levels and roles, allowing Managers to have admin access and Developers to be regular users. The system keeps track of teams, budgets, transactions, and expense categories. Admin users have the ability to fully manage budgets and transactions, while regular users can only create, view, and update relevant data.

## Installation

### Local Installation - To run the web application locally, follow these steps:

#### Prerequisites - Install the following on your machine:

- **Python 3.x**  
   Python is a programming language used to build the application. Follow the instructions here to download and install Python for your device: (https://www.python.org/downloads/)  
   After installation, verify that it was successful by running the following command in your terminal or command prompt:  

   python --version

This command will display the installed Python version.

- **Git** 
Git is a version control system that allows you to track changes in your code and collaborate with others. Follow the instructions here to install Git for your device: (https://git-scm.com/downloads)

After installation, verify that it was successful by running:

git --version

- **Virtualenv** 
Virtualenv is a tool that helps manage dependencies for different projects. It creates isolated environments for your Python projects, preventing conflicts between package versions. You can install Virtualenv using pip (Python’s package manager):

pip install virtualenv

-**PostgreSQL**
PostgreSQL is a powerful relational database system used to store the application’s data. Follow the instructions here to install PostgreSQL for your device: (https://www.postgresql.org/download/)

After installation, verify that it was successful by running:

psql --version

To set up the database, start PostgreSQL and create a user and database by running the following commands in your terminal:

sudo -u postgres psql

Then, within the PostgreSQL shell, run these commands:

# Create a new database user by running:
# Replace your_db_user with your desired username and your_password with a desired password.

CREATE USER your_db_user WITH PASSWORD 'your_password';   

# Create a new database to be used in your application and set the previously created user as the owner:
# Replace your_db_name with your desired database name.

CREATE DATABASE your_db_name OWNER your_db_user;

# Once user and database created quit PostgreSQL by running: 

\q

Update the .env File to use these:
Open your .env file in the project root and update the DATABASE_URL variable with your database connection details in the following format:

DATABASE_URL=postgres://your_db_user:your_password@localhost:5432/your_db_name

Finally apply Database Migrations:
Run the following command in your terminal to apply the database migrations and set up the initial database schema to be used in the app:

python manage.py migrate

--------------

**Heroku CLI** (for deploying or managing the Heroku app)
Heroku CLI is a command-line interface for managing applications hosted on Heroku, a cloud platform. Follow the instructions here to install the Heroku CLI for your device: (https://devcenter.heroku.com/articles/heroku-cli)

After installation, verify that it was successful by running:

heroku --version

**App Installation Steps**
Clone the repository: This step downloads the application code from GitHub to your local machine. Run the following commands in your terminal:

git clone https://github.com/your-repo/team-budget-planner.git
cd team-budget-planner

**Create and activate a virtual environment** :
This isolates your project dependencies. Run the following commands:

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

**Install the dependencies:** 
This step installs all the necessary packages required for the application to run. Run:

pip install -r requirements.txt

**Create a .env file in the project root with the following variables:**
The .env file is used to store sensitive information like your secret key and database connection details. Create a new file named .env in the project folder and add the following :

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url

You can generate a SECRET_KEY using the following command:

python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

**Set up the database using PostgreSQL:**
Ensure you have created a PostgreSQL database and user in the previous steps. Update your .env file with the database connection details. Then run the following command to apply the database migrations:

python manage.py migrate

**Run the development server:**
This command starts a local server that allows you to view the application in your web browser:

python manage.py runserver

**Access the app:**
Once the server is running, open your web browser and navigate to:

http://127.0.0.1:8000

You can now log in or register as a new user and start using the app!



**HOSTED VERSION (Heroku)**
You can access the live version of the application hosted on Heroku here: 

Open the Heroku URL: Navigate to the live application using the link provided above.

Register an account: If you are a new user, follow the registration process. If you already have an account, log in using your credentials.

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