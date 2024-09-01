# loop-tracker

## Endpoints
 1. trigger-report -> url:/trigger-report -> response: status and report_id
 2. report-status -> url:/get-report-status/[report-id] -> response: status
 3. get-report -> url: /get-report/[report-id] -> response: csv file

## mechanism of endpoints
  - trigger-report endpoint triggers the report generation and returns the report id where the report will be asynchronously generated in celery.
  - report-status returns the status of report generation (processing/completed) which can be used for polling
  - get-report return the csv file of the report

## calculation logic
  - uptime and downtimes are calculated for one store at a time(for testing only 10 stores data were calculated and used in report)
  - business hour check is carried through annotations(I have impleted this constrain but assumed stores are open 24*7 since some timings are not appropriate)
  - timezones are handled carefully
  - each active poll is extrapolated as 1 hour uptime

## setup and execution

> clone the code to local repo
```
git clone https://github.com/karan-2004/loop-tracker loop_tracker
```
> create the virtual env using venv module
```
cd loop_tracker
python3 -m venv env
```
> activate the environment and install the required packages
```
source env/bin/activate
pip install -r requirements.txt
```
> creating database migrations and migrating the database(sqlite is used as default db)
```
python manage.py makemigrations
python manage.py migrate
```
> to load data from csv to database custom command csv_loader is used.

> since the csv file is of larger size it can't be stored in github repo.

> create a folder data and store all the three csv files
```
mkdir data
cd data
```
> copy all the three csv files to data folder

> formatting of the timestamp_utc in store status csv need to be changed before loading.

> pandas can be used to chage the formatting

```
import pandas as pd
df = pd.read_csv(file path to store status csv)
df.timestamp_utc = df.timestamp_utc.map(lambda x: " ".join(x.split()[:2]))
df.to_csv(file path to store status csv, index=False)
```
> be aware to use the correct file path

> then the csv can be loaded to db using the following commands
```
python manage.py csv_loader BusinessHour 'file path to business hours csv'
python manage.py csv_loader Timezone 'file path to timezone csv'
python manage.py csv_loader StoreStatus 'file path to store status csv'
```
> celery needs to be started inorder to handle asynchronous task
```
celery -A loop_tracker worker --loglevel=info
```

> start the server
```
python manage.py runserver
```

## THE END.

> now you can start the testing






