# # Summary
# 
# The script taps into the Totango Touchpoints API (documentation available [here](https://support.totango.com/hc/en-us/articles/115000597266-Touchpoints-API))  to archive all touchpoints, notes, and alerts. It starts with obtaining a full client list, then sequentially queries the Touchpoints API for each client to collect associated touchpoints. Post data gathering, basic data cleaning is performed for the readiness of the data for subsequent operations or backup.
# 
# ## Key Features
# 
# 1. Utilizes the Totango Touchpoints API for data extraction.
# <br>
# 2. Gathers a comprehensive list of all clients for processing.
# <br>
# 3. Seqntially pulls all touchpoints, notes, and alerts for each client.
# <br>
# 4. Conducts basic data cleaning post data extraction.
# <br>   
# 5. Aids in the process of backing up crucial client interaction data.

# # Libraries
import datetime
import json
import pandas as pd
import requests
from pandas.io.json import json_normalize

#the autherization token needs to be obtained from totango and passed in the header
headers = {
    'app-token':
    'ENTER YOUR TOKEN HERE',
}

# # Fetching Client List of the Totango Instance

# In this code block, we're going through a range of numbers from 0 to 15000 (Depends on the n, increasing by 1000 at each step. At each step, we're creating a new query with the current offset being the number i. This query is then sent to a URL via a POST request. We get the JSON response
# 
# The use of an f-string in this case helps to inject the value of i directly into the string, making it more readable and efficient than string concatenation.

clientlist = pd.DataFrame()
for i in range(0, 16000, 1000):
    data =  {
    'query':
    f'{{"terms":[{{"type":"string","term":"status_group","in_list":["paying"]}},{{"type":"string_attribute","attribute":"Account Type","query_term_id":"account_type","in_list":["Client"]}}],"count":1000,"offset":{i},"fields":[],"scope":"all"}}'
    }
    response = requests.post(
    'https://app.totango.com/api/v1/search/accounts',
    headers=headers,data=data)    
    data = response.json()
    data = data['response']['accounts']['hits']
    data = pd.json_normalize(data)
    clientlist = clientlist.append(data, ignore_index=True)
    
print("Total Number of Clients Found in Totango", len(clientlist))

# # Fetching Touchpoints

# This code block performs the following steps:
# 
# 1. Initializes an empty DataFrame named df_.
# 
# 2. Sends a GET request to the 'https://app.totango.com/api/v2/events/' endpoint with a specified account_id as a parameter and specific headers. This is intended to fetch data related to a specific account.
# 
# 3. Parses the JSON response from the API request.
# 
# 4. Converts the parsed JSON response to a pandas DataFrame using the pd.json_normalize() function. This flattens the JSON structure into a tabular format.
# 
# 5. Drops all rows in the initialized DataFrame df_ using the drop() function. This is done to ensure that the DataFrame is empty and clean for subsequent use.

#initialize an empty dataframe to hold the touchpoints data
payload = {'account_id':clientlist.name.iloc[0]}
response = requests.get(
    'https://app.totango.com/api/v2/events/', params=payload, headers=headers)
catcherframework = response.json()
catcherframework = pd.json_normalize(catcherframework)
#df_ = pd.DataFrame(index=catcherframework.index, columns=catcherframework.columns)
df_ = pd.DataFrame()
#need to clean the initialized df hence the df is dropped to remove multiple NaN rows
df_.drop(df_.index, inplace=True)

# time.sleep(65) 
# Loop over the range from 0 to the length of the clientlist minus 11610
for i in range(0, len(clientlist)-1): 

    # Create a dictionary payload with account_id key and corresponding value from the client list
    payload = {'account_id': clientlist.name.iloc[i]}

    # Send a GET request to the Totango API with the payload and headers
    response = requests.get('https://app.totango.com/api/v2/events/', params=payload, headers=headers)

    try:
        # Try to convert the response into JSON and normalize it into a flat table
        catcher = response.json()
        catcher = pd.json_normalize(catcher)

        # Concatenate the result with the existing dataframe (df_)
        df_ = pd.concat([df_, catcher], sort=False, ignore_index='True')

        # Print the index and payload for debugging purposes
        print(i, payload)

    except Exception as e:
        # If there's an error during the JSON parsing, print an error message and continue with the next iteration
        print ("JSON Parsing error detected")
        continue

# # Data Cleaning

# The following line converts the timestamp from Totango (which is in Unix time format) to Excel's timestamp.
# This is achieved by adding the date difference between Unix Epoch (1970-01-01) and Excel's zero date (1900-01-01, which is 25569 days) 
# to the Unix time (divided by the number of milliseconds in a day - 86400000, since Unix time is in milliseconds).
df_['exceldate'] = (25569 + df_.timestamp.divide(86400000)) 

# This line converts the Excel date (which is a float number representing the number of days since 1900-01-01) 
# back to a pandas TimedeltaIndex and adds it to the date 1900-01-01. We subtract one from the exceldate because Excel wrongly 
# considers 1900 a leap year.
df_['date'] = pd.TimedeltaIndex(df_.exceldate-1, unit='d') + datetime.datetime(1900,1,1)

# This line extracts only the date part of the datetime object (removing the time component)
df_.date = df_.date.dt.date

#renaming totango field names into a shortened clear name without spaces
df_.rename(columns={
    'account.display_name': 'display_name',
    'account.id': 'account_id',
    'alert_content.alert_type':'alert_type',
    'alert_content.description':'alert_description',
    'alert_content.properties.duration':'alert_duration',
    'alert_content.properties.health':'alert_health',
    'alert_content.properties.health_prev':'alert_health_prev',
    'alert_content.sentiment':'alert_sentiment',
    'id':'touchpoint_id',
    'note_content.note_id':'note_id',
    'note_content.text':'note_text',
    'note_content.totango_user.user_name':'note_created_by',
    'properties.activity_type_id':'activity_type',
    'properties.activity_type_id_is_modified':'is_activity_modified',          
    'properties.activity_type_id_prev':'activity_type_prev',                  
    'properties.last_edit_time':'last_edit_time',
    'properties.last_edit_user':'last_edit_user',                                                                   
    'type':'touchpoint_type',                                               
    'properties.assets':'assets',                                  
    'task_content.action':'task_action',                                
    'task_content.assignee.current':'task_current_assignee',
    'task_content.assignee.is_modified':'is_task_assignee_modified',                  
    'task_content.assigner.current':'task_assigner',                      
    'task_content.assigner.is_modified':'is_task_assigner_modified',                  
    'task_content.description.current':'task_description',                  
    'task_content.description.is_modified':'is_task_desc_modified',               
    'task_content.due_date.current':'task_due_date',                      
    'task_content.due_date.is_modified':'is_task_due_date_modified',                  
    'task_content.last_updater.current':'task_last_updater',                  
    'task_content.last_updater.is_modified':'is_task_updater_modified',             
    'task_content.origin':'task_origin',                                
    'task_content.priority.current':'task_priority',
    'task_content.priority.is_modified':'is_task_priority_modified',                  
    'task_content.status.current':'task_status',                        
    'task_content.status.is_modified':'is_task_status_modified',                    
    'task_content.taskAction':'task_action_final',                            
    'task_content.task_id':'task_id',
    'account.contract_value':'acv',
    'task_content.last_updater.prev':'task_last_updater_prev',                     
    'task_content.status.prev':'task_status_prev',
    'task_content.priority.prev':'task_priority_prev',
    'task_content.assignee.prev':'task_assignee_prev',
    'task_content.description.prev':'task_description_prev',
    'task_content.due_date.prev':'task_due_date_prev'   
},inplace=True)

#adding refreshed date column
df_['refreshed_date']=pd.to_datetime('today')
df_['refreshed_date']=df_['refreshed_date'].dt.date
