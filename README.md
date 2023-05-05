# octopus
Octopus is a tool for managing Linux machines remotely.
Octopus is not a program designed for multi-user consideration.

# Install
### Install python and pip
Please refer to
1. https://www.python.org/downloads/
2. https://pip.pypa.io/en/stable/installation/

### Install and activate venv
```bash
# for installation
python -m venv venv

# for activation
. ./venv/bin/activate
# or
source ./venv/bin/activate
```

### Clone octopus
```bash
git clone https://github.com/munseoplim/octopus
```

### Install python modules
```bash
sudo pip install -r requirements.txt
```

### Migrate database
```bash
python manage.py migrate
```

### Run!
```bash
python manage.py runserver
```
Please connect to https://127.0.0.1:8000


# How to use
### Create admin
```bash
python3 manage.py createsuperuser
```

### Add "ResourceType"
A "Resource" refers to a single machine. A "ResourceType" refers to the classification of the machine. Thus "ResourceType" should be create first.

### Add "Resource" and "ProxyServers"
After that you can add "Resource" as known as a machine. "ProxyServers" is optional. If you want to use proxy servers, you should add them before adding "Resource"

### Add "TestStage"
A "TestStage" refers to the command used to check the status of a resource.

### Check https://127.0.0.1:8000 again
Once all of the above settings are completed, you can check the status of each machine on this page.

### Send a command or files to machines
You can send a command or files when you access https://127.0.0.1:8000/runner.
