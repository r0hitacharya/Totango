# # Totango Segment Data Extraction
# 
# This script is particularly useful for automating the process of extracting and unpacking segment data from Totango. It makes data analysis and manipulation tasks easier by providing clean, segmented data.
# 
# ## Key Features
# The script has the capability to extract two types of segment data from Totango: User Segment and Account Segment. Each type has a unique API endpoint to retrieve the data.
# 
# 1. In the Totango UI, you need to generate the specific API endpoint to fetch the data for the respective segment.
# 
# 2. The data received from the API endpoint is in JSON format. It contains a column named selected_fields which encapsulates multiple data points.
# 
# 3. The script unpacks the selected_fields column and splits it into distinct columns for easier data manipulation and analysis.

# # Libraries

import datetime
import json
import pandas as pd
import requests
from pandas.io.json import json_normalize
from flatten_json import flatten
pd.set_option('display.max_columns', None)

headers = {
    'app-token':
    'ENTER YOUR TOKEN HERE'
}


# # User Type Segment Call


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


# Concatenate all the dataframes in the list into a single dataframe
data = pd.concat(dataframes, ignore_index=True)


#selected_fields contains multiple values in a single columns, hence we need to split the column into individual columns
data['selected_fields'] = data['selected_fields'].astype(str)
data['selected_fields'] = data['selected_fields'].str.replace('[','').str.replace(']','')


#Splitting the selected_fields columns into individual columns
data[[
    'ENTER', 'COLUMNS', 'NAMES', 'HERE'
]] = data['selected_fields'].str.split("',", expand=True)


# # Account Type Segment Call

# Initial empty list to store dataframes
dataframes = []


# Open a new session for sending HTTP requests
with requests.session() as session:
    # Iterate over a range of numbers, starting at 0, ending at 1000000, stepping by 1000
    for i in range(0, 1000000, 1000):
        data = {
      'query': ' {"terms":[{"type":"string_attribute","attribute":"Account Type","in_list":["Contract"]},{"type":"string_attribute","attribute":"Status","in_list":["Active"]},{"type":"simple_date_attribute","joker":"between_next_90_and_200_days","attribute":"Contract Renewal Date"}],"count":1000,"offset":' + str(i) + ',"fields":[{"type":"string_attribute","attribute":"DomainName","field_display_name":"Client Name"},{"type":"string_attribute","attribute":"DomainCountry","field_display_name":"Domain Country"},{"type":"string_attribute","attribute":"Sold To Code","field_display_name":"[FIN] Client Sold To Code"},{"type":"string_attribute","attribute":"BU","field_display_name":"[FIN] Active BUs"},{"type":"number_metric","field_display_name":"[FIN] ACV - Annual Contract Value (Sum)","metric":"sum__contract_value","source":"rollup"},{"type":"simple_date_attribute","attribute":"Contract Renewal Date","field_display_name":"[FIN] Contract Renewal Date"},{"type":"string_attribute","attribute":"ActualStatus","field_display_name":"[FIN] Contract Line Item Status in SAP"},{"type":"string_attribute","attribute":"Contract Header ID","field_display_name":"[FIN] SAP Contract Header ID"},{"type":"string_attribute","attribute":"Contract Line ID","field_display_name":"[FIN] SAP Contract Line ID"},{"type":"string_attribute","attribute":"Sold To Code","field_display_name":"[FIN] Client Sold To Code"}],"scope":"all"}'
    }

        # Create a dictionary 'data' to hold the query and team_id, where the query includes an offset "offset:str(i)"
        # Code for 'data' goes here...

        # Post request to the API endpoint with the defined headers and data
        response = session.post(
            'https://api.totango.com/api/v1/search/accounts',  # See Totango Documentation for URL
            headers=headers,
            data=data)

        # Check if the request was successful (status code 200), if not raise an error
        response.raise_for_status()
        data = response.json()

        # Break if the necessary keys are not in the response
        if 'response' not in data or 'accounts' not in data['response'] or 'hits' not in data['response']['accounts']:
            print("Cannot find the key accounts or hits")
            break

        # Convert the 'hits' list to a DataFrame and append to the list of dataframes
        dataframes.append(pd.json_normalize(data['response']['accounts']['hits']))

        # If the total number of hits is less than or equal to the current offset + 1000, break the loop
        total_hits = data['response']['accounts']['total_hits']
        if total_hits <= i + 1000:
            break


data = pd.concat(dataframes, ignore_index=True)

#selected_fields contains multiple values in a single columns, hence we need to split the column into individual columns
data['selected_fields'] = data['selected_fields'].astype(str)
data['selected_fields'] = data['selected_fields'].str.replace('[','').str.replace(']','')

#Splitting the selected_fields columns into individual columns
data[[
    'ENTER', 'COLUMNS', 'NAMES', 'HERE'
]] = data['selected_fields'].str.split("',", expand=True)