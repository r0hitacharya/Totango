# # Python Script for Fetching and Processing Totango API Data
# # This script serves as a comprehensive Python solution for fetching user data from the Totango Search API, followed by data cleaning, preprocessing, and ultimately converting it into a DataFrame for further data manipulation or analysis.
# # ## Key Functions of the Script:
# # 1. API Data Fetching: The script initiates an API request to fetch the user data. It handles paginated results iteratively to gather a comprehensive dataset.
# # 2. Timestamp Conversion: The Unix timestamp from the 'first_activity_time' field is converted into a more readable datetime format.
# # 3. Data Cleaning: The script removes all single quote characters from the data to prevent potential issues in subsequent data processing or analysis tasks.

# # Libraries and Headers

import requests
import pandas as pd

#Please note that you need to be an totango admin
headers = {
    'app-token': 'YOUR_APP_TOKEN_HERE',  # Please insert your key from Totango here
    'ContentType': 'application/x-www-form-urlencoded'
}


# # Loop

# Initial empty list to store dataframes
dataframes = []

# Open a new session for sending HTTP requests
with requests.session() as session:
    # Iterate over a range of numbers, starting at 0, ending at 1000000 (A very high random number), stepping by 1000
    for i in range(0, 1000000, 1000):
        
         # Create a dictionary 'data' to hold the query and team_id, where the query includes an offset "offset:str(i)"
        data = {
            'query': '{"scope":"all","fields":[{"attribute":"First Name","field_display_name":"First Name","type":"string_attribute"},{"attribute":"Last Name","field_display_name":"Last Name","type":"string_attribute"},{"attribute":"License","field_display_name":"License","type":"string_attribute"},{"type":"string_attribute","attribute":"__internal_status","field_display_name":"Status"},{"type":"string_attribute","attribute":"__internal_role","field_display_name":"Totango Role"},{"attribute":"__internal_teams","field_display_name":"Teams","type":"string_attribute"},{"attribute":"Region","field_display_name":"User Region","type":"string_attribute"},{"attribute":"Country","field_display_name":"Totango User Country","type":"string_attribute"},{"attribute":"NTT Team","field_display_name":"NTT Team","type":"string_attribute"}],"offset":'+str(i)+',"count":1000,"terms":[{"type":"string_attribute","attribute":"__internal_status","in_list":["Active","Created","Disabled"]}]}',
            'team_id' : -1
        }
        
        # Post request to the API endpoint with the defined headers and data
        response = session.post(
            'https://api.totango.com/api/v1/search/users/internal', # See Totango Documentation for URL
            headers=headers,
            data=data)
        
        # Check if the request was successful (status code 200), if not raise an error
        response.raise_for_status()
        data = response.json()
        
        # Break if the necessary keys are not in the response
        if 'response' not in data or 'users' not in data['response'] or 'hits' not in data['response']['users']:
            print("Cannot find the key users or hits")
            break
            
        # Convert the 'hits' list to a DataFrame and append to the list of dataframes
        dataframes.append(pd.json_normalize(data['response']['users']['hits']))

        # If the total number of hits is less than or equal to the current offset + 1000, break the loop
        total_hits = data['response']['users']['total_hits']
        if total_hits <= i + 1000:
            break


# # Consolidating the Looped Data

# Concatenate all the dataframes in the list into a single dataframe
data = pd.concat(dataframes, ignore_index=True)

#selected_fields contains multiple values in a single columns, hence we need to split the column into individual columns
data['selected_fields'] = data['selected_fields'].astype(str)
data['selected_fields'] = data['selected_fields'].str.replace('[','').str.replace(']','')

#Splitting the selected_fields columns into individual columns
data[[
    'first_name', 'last_name', 'license', 'status', 'totango_role', 'teams',
    'user_region', 'totango_user_country', 'ntt_team'
]] = data['selected_fields'].str.split("',", expand=True)

data['name'] = data['first_name'] +' '+data['last_name']

# # Cleaning

# 'first_activity_time' is assumed to be a Unix timestamp in milliseconds.
# First, convert it to days by dividing it by the number of milliseconds in a day (86400000).
# Add this to 25569, which is the number of days between the Unix epoch (1970-01-01) and the Excel epoch (1900-01-01, 0-indexed).
# Subtract 1 because Unix epoch is 1-indexed. This gives us the number of days since the Excel epoch.
# Convert this to a TimedeltaIndex, which represents a duration or elapsed time.
# Add the Excel epoch (1900-01-01) to get the correct date.

data['first_activity_time'] = pd.TimedeltaIndex((25569 + data.first_activity_time.divide(86400000))-1, unit='d') + datetime.datetime(1900,1,1)
data['first_activity_time'] = data['first_activity_time'].dt.date

data['last_activity_time'] = pd.TimedeltaIndex((25569 + data.last_activity_time.divide(86400000))-1, unit='d') + datetime.datetime(1900,1,1)
data['last_activity_time'] = data['last_activity_time'].dt.date

# Iterate over the DataFrame's columns with their corresponding index
for i, col in enumerate(data.columns):
    # For each column, convert the entire column to string type
    # and then replace single quotes with nothing.
    # data.iloc[:, i] is used to select the i-th column of the DataFrame.
    data.iloc[:, i] = data.iloc[:, i].astype(str).str.replace("'", '')
