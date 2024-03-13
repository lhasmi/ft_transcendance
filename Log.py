# before all  run following steps
# brew install mysql && brew install mariadb
# pip install mysqlclient

#	To start mariadb :	brew services start mariadb
#	Or, if  don't want/need a background service you can just run:
#  		/usr/local/opt/mariadb/bin/mysqld_safe --datadir\=/usr/local/var/mysql
# run the mariadb_secure_installation  to secure your database server, 
# including setting the root password, removing anonymous users, disallowing 
# root login remotely, and removing test databases. I chose no for all above. 
# 	Create a Database and User for Django
# 		mysql -u root -p   then   CREATE DATABASE my_django_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# 	CREATE USER 'lhasmi'@'localhost' IDENTIFIED BY 'lh'; then FLUSH PRIVILEGES;

# Configure Django to use MySQL/MariaDB
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_django_project',
        'USER': 'lhasmi',
        'PASSWORD': 'lh',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}'''
# Migrate Django’s Built-in Apps
# 		python3 manage.py migrate

############################################
#### In Total today : 13.03.2024
############################################
# I've installed Django and connected it to a MariaDB database.
# I've run migrations, indicating Django project is configured correctly to communicate with  database.

############################################
# NEXT: 
############################################

# For development, I can use Django's built-in server. 
# For production, consider learning about deploying Django with Apache and mod_wsgi.
# Consider using a virtual environment for Django development if you haven't already.