# Team Budget Planner - Instructions

# 1. Clone the Repository
# Clone the project repository from GitHub (or unzip the provided archive)
git clone <repository_url>
cd team_budget_planner

# 2. Set Up the Virtual Environment
# Create and activate a virtual environment to isolate your project dependencies
python3 -m venv env
source env/bin/activate  # For MacOS/Linux
# For Windows
# env\Scripts\activate 

# 3. Install Dependencies
# Install the required dependencies from the requirements.txt file
pip install -r requirements.txt

# 4. Set Up Environment Variables
# Create a .env file in the project root and add the required environment variables
# Use your own values for the variables below
echo "SECRET_KEY=your-secret-key" > .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1,<production-domain>" >> .env
echo "DATABASE_URL=your-database-url" >> .env

# 5. Migrate the Database
# Run the database migrations to create the necessary tables
python manage.py migrate

# 6. Create a Superuser (Admin Account)
# Create a superuser to manage the application via the Django admin panel
python manage.py createsuperuser

# 7. Run the Development Server
# Start the Django development server locally
python manage.py runserver

# Access the Application
# Open your web browser and go to:
# Local Development: http://127.0.0.1:8000
# Production: https://<app-name>.herokuapp.com

# Deploying to Heroku

# 1. Log In to Heroku
# Log in to Heroku using the CLI
heroku login

# 2. Create a Heroku App
# Create a new Heroku app
heroku create <app-name>

# 3. Set Heroku Environment Variables
# Set the required environment variables on Heroku
heroku config:set SECRET_KEY=your-secret-key

# 4. Deploy the Application
# Push your project to Heroku
git push heroku main

# 5. Apply Database Migrations on Heroku
# Once deployed, run migrations on Heroku
heroku run python manage.py migrate

# 6. Access the Production Application
# Visit the live app on Heroku:
# https://<app-name>.herokuapp.com
