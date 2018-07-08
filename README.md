# hisaab
It is a project which Helps us manage all the expenses, trasactions, and payments across the different NavGurukul facilities.

# Getting Started
Open console(IDE) on your machine, first of all you have to clone this repository on your machine for that make directory or project folder on
you machine through console then for cloning this repo :
On GitHub, navigate to the main page of the repository.
Under the repository name, click Clone or download.
In the Clone with HTTPs section, copy the URL for the repository
Type git clone, and then paste the URL you copied in Step 2.
Press Enter. Your local clone will be created, so the cloning part is done.

```
This project is made on the Python framework django so some installation you have to made for smooth running of the project :
open console run the commands,

1. sudo apt-get install python
2. sudo apt-get install pip #pip is a package manager for python.
3. pip install --upgrade pip #For Upgrading pip file.
4. pip install django~=1.11.0 #installing django.
5. pip install social-auth-app-django 
6 pip install python-social-auth[django]
7. pip install Pillow # we install pillow for images
8. sudo apt-get install mysql-client
9. sudo apt-get install python-mysqldb
10. pip install django-storages
11. pip install boto3
```

So, installation part is done now for running he app on web browser we have to do :

```
1. Open colsole
2. Navigate to the hisaab/Hisaabproject directory
3. Execute "python manage.py runserver"
4. Open web browser and type localhost:8000

```

Additionally, to set up the server:

```
sudo apt-get install nginx

Edit nginx configuration using command:
sudo nano /etc/nginx/sites-available/hisaab

Paste following configuration in that file
server {
        listen 80;
        server_name hisaab.navgurukul.org;
        location / {
                proxy_pass http://localhost:8000;
        }
}

Save the file.

Add the following lines into /etc/sysctl.conf file:

# allow processes to bind to the non-local address
# (necessary for apache/nginx in Amazon EC2)
net.ipv4.ip_nonlocal_bind = 1
and then reload your sysctl.conf by:

sudo sysctl -p /etc/sysctl.conf

cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/hisaab hisaab
sudo service nginx reload
sudo service nginx restart

```
