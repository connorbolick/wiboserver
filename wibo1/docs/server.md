# Wibo Documentation: Server Setup

## Terms

BitBucket
: a hosting site for the distributed version control system (DVCS) Git. [bitbucket.org](https://bitbucket.org)

Django
: a web application framework for Python. [django.org](http://django.org)

Git
: a distributed version controll system. [git-scm.org](http://git-scm.org)

Python
: a programming language. [python.org](http://python.org)

## Setting Up the Server
At it's core, Wibo is nothing more than a web application that serves as an interface for a database. There are two ways to run Wibo: in production and in development. To set up a computer to host Wibo so it can be accessed from other computers follow the "production" instructions below. To test new features or updates, follow the "development" instructions. As with most things involving computers, the instructions below were out of date before they were written. Getting things to actually work may take some time...and may not be as easy as these instructions make it out to be.

**Note:** I'm assuming you have a few things preinstalled on your system (like Python 2.\* and Git). They should be installed on most \*nix systems out of the box. If something doesn't work though, you may have to check. Also, most of the open source software Wibo uses was designed to run on Linux systems, so getting everything installed on a Mac is...interesting. Good luck, you have my sympathy.

### Terms
Gunicorn
: "green unicorn" is a Python WSGI HTTP server. [gunicorn.org](http://gunicorn.org)

MySQL
: an open source relational database. [mysql.com](http://mysql.com)

Nginx
: "engine x" an HTTP proxy server. [nginx.org](http://nginx.org/en)

PIP
: a tool for installing and managing Python packages. [Package Index](https://pypi.python.org/pypi/pip)

VirtualEnv
: a tool created to isolate Python environments. [virtualenv.org](http://www.virtualenv.org/en/latest)

### Download the Source Code
The source code is hosted in the [CB+D BitBucket repository](https://bitbucket.org/cbplusd/wibo). 

First create a directory to hold repositories on your computer. In your home directory (/Users/<USERNAME>/) create a directory named "repos". Within that directory create another directory that will hold the specific repository you're going to be working with (this will be something like "wibo\_master" or "wibo\_dev"). **Note:** I'm assuming the production version of the code will be in /Users/USERNAME/repos/wibo\_master for the rest of this documentation.

Open a terminal window and navigate to the repository directory you just created. Then clone the repo with:

    git clone https://bitbucket.org/cbplusd/wibo.git

You can now edit away to your heart's content, but there are a few more steps before you can run or even test the code.

### Setup the Virtual Environment
VirtualEnv lets you setup and run multiple versions of Python packages. For Wibo, this makes sure you have the right version of every required package installed. To get everything running, you'll need to download the virtualenv.py file and create a new virtual enviroment.

In a terminal window:
    
    curl -0 https://pypi.python.org/packages/source/v/virtualenv-X.X.tar.gz
    tar -zxvf virtualenv-X.X.tar.gz
    cd virtualenv-X.X

    python virtualenv.py ~/wibo-env --no-site-packages --distribute

**Note:** At the time of this writing (2/27/14) Wibo was running from a different virtualenv. So if you're trying to fix what's already running, replace wibo-env with wibo-deploy.

To activate this environment, open a terminal window and type:

    source ~/wibo-env/bin/activate

Next we need to install the packages we'll actually be using. Python has an awesome package manager called PIP which can read package requirments from a file. 

In a terminal window, activate the Wibo environment, then navigate (cd) to the source directory and type:

    pip install -r requirments.txt


### In Production

To host Wibo so other computers have access to the app, a full web server must be installed. The following is how we set things up at CB+D.

Nginx is handles incoming requests, which get passed along to Gunicorn. Gunicorn runs the Python/Django code to return an apporpiate html document. The configurations listed are working as of 11/25/13.

#### Terms
Homebrew
: an open source package manager for OS X. [brew.sh](http://brew.sh)

Plist
: a "property list" file used to store data (OS X uses plist files to hold information on programs that should start up or run automatically).

Symbolic Link
: a special file that links or redirects to another file.

#### Install Nginx
Nginx is what handles incoming requests from other machines. 

##### Install Homebrew
Follow the instalation instructions on [brew.sh](http://brew.sh). 

Run in a terminal window:

    ruby -e "$curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

##### Install and Configure Nginx
More details can be found [here](http://learnaholic.me/2012/10/10/installing-nginx-in-mac-os-x-mountain-lion/). 

In a terminal window:

    brew install nginx

Homebrew puts the configuration file for Nginx at /usr/local/etc/nginx/nginx.conf. Edit it so it reads:

    worker_processes  1;

    events {
        worker_connections  1024;
    }


    http {
        include       mime.types;
        default_type  application/octet-stream;

        sendfile        on;

        keepalive_timeout  65;

        
        include /Users/USERNAME/SERVER DIRECTORY/sites-enabled/*;

    }

Create a directory to store active and available website conf files. I'm assuming it will be in your user home directory (/Users/USERNAME). You should create the directory structure below:

    /Users/USERNAME/

    |- SERVER DIRECTORY
      |- sites-available
      |- sites-enabled

In the sites-available directory create a file named "wibo" and edit it to contain:

    # file: /Users/USERNAME/wibo-server/sites-available/wibo 
    # nginx configuration for wibo 

    upstream app_server {
      server localhost:8000 fail_timeout=0;
    }

    server { 
      listen 80;
      server_name localhost; 
      access_log /usr/local/Cellar/nginx/1.2.6/logs/access.log; 
      error_log /usr/local/Cellar/nginx/1.2.6/logs/error.log;

      root /User/USERNAME/repos/wibo_master/wibo;

      location /site_media/static { 
        alias /Users/USERNAME/repos/wibo_master/wibo/wibo/site_media/static;
      }

      location /site_media/media { 
        alias /Users/USERNAME/repos/wibo_master/wibo/wibo/site_media/media;
      } 
      location / { 
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_connect_timeout 20000;
        proxy_read_timeout 20000;
        proxy_pass http://localhost:8000/;
      } 

    }

In a terminal window, navigate to the "sites-enabled" directory and create a symoblic link to the "wibo" file with the command:

    ln -s ../sites-available/wibo

Next you want to set Nginx to run every time you log in. To do this, create a plist file in /Users/USERNAME/Library/LaunchAgents called "homebrew.mxcl.nginx.plist". It should contain:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>Label</key>
        <string>homebrew.mxcl.nginx</string>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <false/>
        <key>UserName</key>
        <string>USERNAME</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/opt/nginx/sbin/nginx</string>
            <string>-g</string>
            <string>daemon off;</string>
        </array>
        <key>WorkingDirectory</key>
        <string>/usr/local</string>
      </dict>
    </plist>

Restart your computer and the server should start running when you log in. To test it open a web browser and type [localhost](http://localhost). You should get a 502 gateway error.

#### Green Unicorn
Green Unicorn is what will actually run the Python/Django code. It was installed a few steps ago (see Setup the Virtual Environment), but we need to do a few more things to get it running.

We want Green Unicorn to run when the computer boots, so create another plist file in /Library/LaunchDaemons called "edu.clemson.gunicorn.plist". It should contain:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>edu.clemson.gunicorn</string>
        <key>ProgramArguments</key>
        <array>
            <string>/Users/USERNAME/wibo-env/bin/gunicorn_django</string>
            <string>--workers=4</string>
            <string>/Users/USERNAME/repos/wibo_master/wibo/wibo/settings.py</string>
        </array>
        <key>KeepAlive</key><true />
        <key>StandardErrorPath</key><string>/Users/USERNAME/wibo-server/wibo.error.log</string>
        <key>StandardOutPath</key><string>/Users/USERNAME/wibo-server/wibo.access.log</string>
    </dict>
    </plist>

**Note:** the 'workers' agrument above is the number of processors to give Green Unicorn. More processors means more people can be requesting information from Wibo at the same time, but it also means the machine running Wibo might be slower for other tasks (like Photoshop).

#### MySQL
MySQL is the database that holds all of the actual data for Wibo. After installing it, you'll need to create a database user/password for Wibo.

##### Install MySQL
I tried to find a nice scriptable way to install MySQL on a Mac and couldn't (at least not at the scale we needed it). So you'll have to install it manually.

Go to [dev.mysql.com/downloads/mysql](http://dev.mysql.com/downloads/mysql) and download the latest DMG Archive for your architecture (either 32-bit or 64-bit depending on your computer). Double click on the downloaded package, then the main MySQL installation package and follow the instruction on screen. When the setup asks you for a root password, make sure you remember what you type in. We'll need it to set up the Wibo user.

You'll also want to install the MySQL Startup Item. This should be included in the same package. Just double click the MySQLStartItem.pkg file. You may have to restart your computer for the changes to take effect

##### Create the Wibo Database and User
To create a new MySQL user, log in to MySQL using the 'root' user and the password you entered when you installed MySQL. Open a terminal window and type (replace PASSWORD with your password):
    
    mysql -u root -pPASSWORD

Then create a new database with the command:
    
    CREATE DATABASE wibo;

Then create a new user and add it to the Wibo database with the command (replace WIBOPASSWORD with the password you want Wibo to use to access the database):

    CREATE USER 'wiboAdmin'@'localhost' IDENTIFIED BY 'WIBOPASSWORD';
    GRANT ALL ON wibo.* to 'wiboAdmin'@'localhost';

#### Local Settings File
Django uses a settings.py file that runs the server connections. The settings.py file in the source repository is enough to get you started, but to get a production version running, you'll need to extend that file. 

In a terminal window navigate to the source directory. In the 'wibo' directory create a file called 'local_settings.py' that contains:

    DEBUG = False

    ADMINS = [
        # ("Your Name", "your_email@example.com"),
    ]

    MANAGERS = ADMINS

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "wibo",
            "USER": "wiboAdmin",
            "PASSWORD": "WIBOPASSWORD",
            "HOST": "",
            "PORT": "",
        }
    }

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = ""

    THEME_ACCOUNT_CONTACT_EMAIL = "cbplusd@clemson.edu"

    MATERIAL_DESIGN_PRINTED = 1 #343
    MATERIAL_DESIGN_NPRINTED= 1 #342

#### Test it Out
Everything should be set up now. In a web browser, go to [localhost](localhost). You should see the "Welcome to Wibo" page. To access Wibo from another computer you just need to open a web browser and type the server computer's IP address into the navigation bar. 

**Note:** you may need to reconfigure your firewall/network settings to allow incoming http connections on port 80. I didn't have to, but be aware that may be an issue.

### In Development
#### Terms
SQLite
: a software library that implements a self-contained, serverless, trasactional SQL database engine. [sqlite.org](http://www.sqlite.org)

The development environment is much easier to set up. For testing stuff out you can just use Django's built in database and web servers. It uses Python's SQLite3 backend.

#### Local Settings File
Django uses a settings.py file that runs the server connections. The settings.py file in the source repository is enough to get you started, but some features may not work correctly out of the box.

In a terminal window navigate to the source directory. In the 'wibo' directory create a file called 'local_settings.py' that contains:

    ADMINS = [
        # ("Your Name", "your_email@example.com"),
    ]

    MANAGERS = ADMINS

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = ""

    THEME_ACCOUNT_CONTACT_EMAIL = "cbplusd@clemson.edu"

    MATERIAL_DESIGN_PRINTED = 1 #343
    MATERIAL_DESIGN_NPRINTED= 1 #342

#### Run the Server
To test how Wibo works, start the server.

In a terminal window, navigate to the source directory and:

    python manage.py runserver

Then go to [localhost:8000](localhost:8000) in a web browser.

The terminal window will print out the messages (both successful and error messages) to the screen. You can use it to monitor problems Wibo may encounter while you're developing. No one will be able to access what you're working on until you update the production server.

Press control+C to close the development server (and that's 'control' not 'command').

## Updating the Code
### Making Edits
### Testing
### Commiting Revisions
### Updating the Production Server
#### update_production.py
#### Git Pull
#### Syncdb
#### Migrate Database
#### Restart Green Unicorn

