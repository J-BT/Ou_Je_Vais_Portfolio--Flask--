# Project presented for the following certifications RS3497 “Built a database” and RS3508 “Manage a database” of Digifab school  : Ou Je Vais 


## | Installation

1. Download and install PostgreSQL at the following adress : 
https://www.postgresql.org/download/, according to your OS (Windows, Linux or MacOS)

2. Create a `.env` file and insert the following while replacing {} .

	URI_POSTGRES = postgresql://{your_user_name}:{your_password}@localhost:5432/{your_database_name}

	CLE_SECRETE = {your_secret_key}

	CLE_OPENWEATHER_1 = "{ your OpenweatherMap token}"
	CLE_OPENWEATHER_2 = {your 2nd OpenweatherMap token, if you've got one}

3. Install Python from https://www.python.org/downloads/

4. (Linux) Install python env with apt package : `sudo apt install python3.8-venv`

5. Enter the following command in the terminal prompt : `python3 -m venv (your_virtual_environment)`.
It will create a virtual environment named `your_virtual_environment`

6. Activate your virtual environment :
`source (your_virtual_environment)/bin/activate`
nb:  To deactivate it : enter `deactivate`

7. Install all libraries with pip :
`pip install -r requirements.txt`

8. Update `pip` if necessary.

9. Create the migration file :  `flask db init`

10. Create your 1st migration :  `flask db migrate -m "{your_text} "`

11. Save it : `flask db upgrade`
or cancel it : `flask db downgrade`

12. Create all tables :  `flash shell` then `db.create_all()`

13. Populate them importing  `populate_all_tables` function from the root folder
entering the following command : `from app.models import populate_all_tables`, 
the enter :  `populate_all_tables()` (After few minutes all tables will be populated )

14. Finally launch the app from the root folder entering the following :
`flask run`

## | Deploy with NGINX on a Ubuntu server 20.04

(source DigitalOcean : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04-fr )

1. Create a wsgi file :
Go at the root folder,then enter : `nano ~/{your_project_name}/wsgi.py`.
Please check the file contains the following :
`if __name__ == "__main__":`
`    app = create_app()`
`    app.run()`

2. Create a systemd service unit file:
`sudo nano /etc/systemd/system/{your_project_name}.service`

3. Activate the project to start it on every boot :
`sudo systemctl start {your_project_name}`
then enable it:
`sudo systemctl enable {your_project_name}`

4. Configure NGINX and link your project to a domain name:
- `sudo nano /etc/nginx/sites-available/{your_project_name}`
- `sudo ln -s /etc/nginx/sites-available/{your_project_name} /etc/nginx/sites-enabled`
 
5. Check if the syntax is correct : `sudo nginx -t`

6. Restart NGINX : `sudo systemctl restart nginx` 

## | Description

Based on OECD and OpenWeatherMap, the online service providing global weather
data, APIs, this application create a world countries ranking according to
your favorite criteria.

For now, you can choose among the following criterias:

- Number of inhabitants
- Life expectancy
- Unemployment rate
- Temperature
- Weather conditions

You will be displayed the 10 first countries in a table, then 4 charts that
analyse the first ranked country.




