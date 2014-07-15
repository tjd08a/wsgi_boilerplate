# WSGI Boilerplate
A basic web application which takes the keys and values present in a form and outputs them as text.  
Tests to see if WSGI is working and its basic functionality.

## Setup
The environment used to test this code consisted of the following:
* Operating System: **Ubuntu Server 14.04**
* Web Server: **Apache 2.4.7**
* WSGI Server/Module: **mod_wsgi**

To install Apache run this command:
```
sudo apt-get install apache2
```

To install mod_wsgi run these commands:
```
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod mod-wsgi
```

# Configuration
Apache must be properly configured to run mod_wsgi. The directives below must be added to the config file:
```
WSGIScriptAlias /url/ /path-to-scripts/
<Directory /path-to-scripts>
Require all granted
</Directory>
```

Notes:
* **path-to-scripts** is the location on the server where the scripts are stored.
* **url** is the location that an html reference can link to in order to access the script.

# Troubleshooting
* In older versions of Apache (2.3 and lower), the directive in place of
```
Require all granted
```
was instead:
```
Order allow,deny
Allow from all
```
* Errors in Python scripts will result in "Internal Error" messages from the server.   
  Check the error logs for more information about the Python errors.
