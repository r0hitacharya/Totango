# # Totango SuccessPlay Data Extraction
# 
# ## Summary
# This script is designed to automate the extraction of SuccessPlay statistics from Totango, utilizing the app.totango.com/api/v3/tasks/export/csv?query API. The key feature is the conversion of manual data extraction process from the UI into an automated script-based approach.
# 
# ## Key Features
# 
# 1. Utilizes Totango's tasks/export API to fetch SuccessPlay data.
# 
# 2. The script makes use of a GET request with query parameters that can be obtained from the browser URL when downloading SuccessPlay data manually.
# 
# 3. Automates the extraction of SuccessPlay data, saving time and providing an easily repeatable process.
# 
# 4. Allows easy integration of the data extraction process into larger workflows.
# 
# 5. Enables possibilities for in-depth analysis, reporting, and optimization of customer success strategies.

# # Libraries

import csv
import datetime
import io
import json
import pandas as pd
import requests
from pandas.io.json import json_normalize



# # API Calls

#the autherization token needs to be obtained from totango and passed in the header
headers = {
    'app-token':
    'PUT YOUR TOKEN HERE',
}


# This API call retrieves the data from the Totango service.
# It queries for tasks with specific 'automation_id' values, and orders the output by 'automation_id'.
# It also specifies the fields (columns) to be included in the output CSV file.
#  The URL below can be obtained when you click the export button in the browser, we need to grab the URL quickly from the URL bar

data = requests.get(
    'https://app.totango.com/api/v3/tasks/export/csv?query={%22automation_id%22:[%22ab12cd3e-1234-567f-8999-8d00387a93ac%22,%22a08873d9-55bc-494d-bf79-6d88078913fc%22,%22aa905794-b48a-43e8-81ff-1fab2c4429e8%22,%225d7a6802-efd9-48d0-a329-68a3d623a5b7%22,%2276c2b0a5-66e7-44c3-9c5c-756da34ff927%22,%22045e9c27-cb71-44fe-b0dc-55ed5df1bef0%22,%22b25ccfe0-366b-4508-bf8a-7f7fa90de2cd%22],%22orderBy%22:%22automation_id%22}&fields=[{%22value%22:%22name%22,%22label%22:%22Success%20Play%22},{%22value%22:%22title%22,%22label%22:%22Task%20Title%22},{%22value%22:%22description%22,%22label%22:%22Task%20Description%22},{%22value%22:%22account_display_name%22,%22label%22:%22Account%20Name%22},{%22value%22:%22account_id%22,%22label%22:%22Account%20ID%22},{%22value%22:%22parent_id%22,%22label%22:%22Parent%20Account%20ID%22},{%22value%22:%22status%22,%22label%22:%22Status%22},{%22value%22:%22assignee%22,%22label%22:%22Assigned%20To%22},{%22value%22:%22assigner%22,%22label%22:%22Assigned%20By%22},{%22value%22:%22priority%22,%22label%22:%22Priority%22},{%22value%22:%22create_date%22,%22label%22:%22Date%20Created%22},{%22value%22:%22completed_date%22,%22label%22:%22Date%20Completed%22},{%22value%22:%22due_date%22,%22label%22:%22Due%20Date%22}]&fileName=SuccessPlays',
    headers=headers)

# The response from the API call is a string representing a CSV file.
# This string is converted into a file-like object using 'io.StringIO', and then read into a pandas DataFrame.
call_one = pd.read_csv(io.StringIO(data.text))


# This API call retrieves different data from the Totango service.
# It queries for tasks associated with a specific 'sbId' value (930), and orders the output by 'automation_id'.
# It does not specify the fields to be included, so the default fields will be included in the output CSV file.
data = requests.get(
    'https://app.totango.com/api/v3/tasks/export/csv?query={%22sbId%22:930,%22orderBy%22:%22automation_id%22}&fileName=SuccessPlays',
    headers=headers)

# Again, the response from the API call is read into a pandas DataFrame.
call_two = pd.read_csv(io.StringIO(data.text))


# ## All Successplays

#Successplays needs to be sourced from different groups in totango which can be concatenated in this step
successplays = pd.concat([call_one, call_two], sort=False, ignore_index=True)
print("Concatenation of Successplays from all regions Finished")


#This is the sample list of all columns available in a successplay data dump
print(successplays.columns.tolist())


# # Rename and Assign proper data types


#rename columns to remove space in between column names
successplays.rename(columns={
    'Success Play':'success_play',
    'Task Description':'task_description',
    'Account Name':'account_name',
 'Account ID':'account_id',
 'Parent Account ID':'parent_account_id',
 'Status':'status',
 'Assigned To':'assigned_to',
 'Assigned By':'assigned_by',
 'Priority':'priority',
 'Date Created':'date_created',
 'Date Completed':'date_completed',
 'Due Date':'due_date',
 'Task Title':'task_title'
},inplace=True)


# Remove rows from the 'successplays' DataFrame where 'due_date' is 'Invalid date'
successplays = successplays[successplays.due_date != 'Invalid date']

# Convert the 'date_created' column from string type to datetime type
successplays.date_created = pd.to_datetime(successplays.date_created)

# Convert the 'date_completed' column from string type to datetime type
successplays.date_completed = pd.to_datetime(successplays.date_completed)

# Convert the 'due_date' column from string type to datetime type
successplays.due_date = pd.to_datetime(successplays.due_date)

# Add a new column 'refreshed_date' to the 'successplays' DataFrame, setting its value to today's date
# This can be useful for tracking when the DataFrame was last updated
successplays['refreshed_date'] = pd.to_datetime('today')

# Remove the time part from the 'refreshed_date' column, keeping only the date
# This is because SQL Server doesn't support DateTime with timezone information, and the time part isn't necessary in this case
successplays['refreshed_date'] = successplays['refreshed_date'].dt.date

# Raw Data for Export
successplays.to_csv(
     'Successplays.csv',index=False
)
