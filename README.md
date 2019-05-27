#Teacher Dashboard

Display some information about assignment results

## Installation

### Docker
requires:
* Docker version 18.09.6 or above 
(might work with older versions too)

```sh
sudo docker-compose up 
```
in the project directory. this will spin up the whole application.
You can browse to http://localhost:5000

### locally
requirements:
* A running mongo db server
* python 3
* pip
* virtualenv


You need to have a mongodb
configure the connection string by editing the file config.py
set CONNECTION_STRING to your Mongo database's connection string.

```sh
mkdir venv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python populate_database.py
```
This will create a virtual environment, install requirements, and populate the database.

To run use 
```sh
python app.py
```

## Usage
browse to http://localhost:5000

The application displays four graphs.

Scatter graph of result for all submissions, groupped by student and module, displayed as grade over submission date.

Scatter graph of submissions of a single student, groupped by module, displayed as grade over submission date.

Bar chart showing the final (top grade) score for each student in both modules

Histogram displaying the distribution of final grades in each range. This does not include submissions with zero grade.
