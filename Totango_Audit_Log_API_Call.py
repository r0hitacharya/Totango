#Totango Audit Log API Interaction

#Libraries
import datetime
import json
import pandas as pd
import requests
from pandas.io.json import json_normalize
from dateutil.relativedelta import relativedelta

#Determining Start and End Date for API Parameters
#determine start and end date to be passed onto parameter for the API
#if a particular date is required replace the start and end variable with date in yyyy-mm-dd format
today=datetime.date.today()
start = today - relativedelta(months=1)
start = start - relativedelta(days=today.day-1)
end = today - relativedelta(months=0)
end = end - relativedelta(days=today.day)

print("Pinging AuditLog with the following date range")
print ("Start_date: (>=)",start,"End_date: (<)",end)


#API Call
#the autherization token needs to be obtained from totango and passed in the header
headers = {
    'app-token':
    'PLACE YOUR TOKEN HERE',
}

params = (
    ('startDate', start),
    ('endDate',end),
 )

response = requests.get('https://api.totango.com/api/v2/audit', headers=headers, params=params)


# Convert the API response to a JSON object
data = response.json()

# Normalize semi-structured JSON data into a flat table
data = pd.json_normalize(data)

# Convert the 'timestamp' column in the DataFrame to datetime format for better manipulation
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Capitalize the first letter of each word in the 'action' column of the DataFrame
data.action = data.action.str.title()
