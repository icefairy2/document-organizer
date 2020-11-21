# Document scanner and organizer
Raspberry Pi and multitouch table based document organizer for the project at Next Generation User Interfaces lecture.

## Table of contents
+ [Development setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Virtual environment](#virtual-environment)
  - [Backend](#backend)
  - [Frontend](#frontend)

## Development setup
### Prerequisites
Install Python 3 from: https://www.python.org/downloads/ 

Install Node.js and NPM from: https://nodejs.org/en/download/ 

Verify your installations with:
```
python --version
node -v
npm -v
```

Install your preferred IDEs for development, I use **Pycharm** for *python* and **VS Code** for *React*. The last one is a preference, you can edit the React code from Pycharm just as well.

### Virtual environment
Create virtual environment, either:
1. From **Pycharm** from bottom right corner, click on your *Python version->Add interpreter...*, leave the defaults and click *OK*
2. From command line:
```
pip install virtualenv
virtualenv venv
```

Activate the virtual environment in the command line:
- Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`
> **Note:** the terminal in Pycharm should be in the *venv* by default, you can see *(venv)* at the start of the line

Deactivate: `deactivate`

> **Note:** *venv* is the name of the virtual environment and can be something else. I advise you to call it *venv* to avoid accidentally pushing it to the repository, since only *env* and *venv* are ignored by git.

### Backend
```
pip install -r requirements.txt
```
If the above command fails, install all packages from the file with 
```
pip install <package-name>
```

To generate the database:
```
python manage.py migrate
```

To start the backend, go to folder *backend* and run:
```
python manage.py runserver
```

Create folder _scanned_documents_ under *document-organizer/backend*.

### Frontend
Go to folder *frontend*.

To install dependencies run:
```
npm install
```

To run the development server for the frontend, run the following command:
```
npm run start
```
