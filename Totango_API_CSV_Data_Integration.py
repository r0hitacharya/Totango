import csv
import http.client
import pyodbc
import sqlalchemy
import sqlalchemy as db
from sqlalchemy import event

#DefiningTrigger_CDH_API Functon

#Define a limit for the number of records processed at a time.
PROCESSED_LIMIT = 100

# Function to trigger CDH API
def Trigger_CDH_API(data, Token, Service_id):
      
    # Create a secure HTTPS connection to the int-hub at totango.com
    conn = http.client.HTTPSConnection("int-hub.totango.com")
    
    # The payload is the data we want to send, taken from the function's arguments
    payload = data

    # Define headers for the HTTP request
    headers = {
        'content-type': 'application/json',
        'Authorization': 'app-token ' + #Please Enter 64 char Token Here
        'service_id': #Please Enter Service ID of your Totango instance only numbers e.g. 'service_id': '12345'
    }

    # Make a POST request to the "/api/v1/accounts" endpoint with the payload and headers
    conn.request("POST", "/api/v1/accounts", payload, headers)

    # Get the HTTP response
    res = conn.getresponse()

    # Read the response data
    data = res.read()

    # Print the response data, decoding it from bytes to string
    print(data.decode("utf-8"))


#Establishing Connection and Triggering CDH API

#Define your service id and token
Service_id = 12345
Token = #Enter your token here in double quotes

# Open the CSV file
with open('C:/Users/PUT_YOUR_CSV_HERE.csv', 'r') as f:
    # Use csv.DictReader to read the CSV file
    d_reader = csv.DictReader(f)

    # Get fieldnames from DictReader object and store in list
    headers = d_reader.fieldnames

    # Get the first column Id
    col_Id = headers[0]

    # Print the headers
    print(headers)

    # Initialize variables
    rows_processed = 0
    acc_json = ''

    # Loop through each line in the CSV reader
    for line in d_reader:
        in_attributes = False
        rows_processed += 1

        # Loop through each column in the headers
        for col in headers:
            if (col == col_Id):
                # If not the first row, append a comma to the JSON string
                if (rows_processed > 1):
                    acc_json += ','
                # Start a new JSON object for the account
                acc_json += '{"id": "' + line[col_Id] + '","attributes": {'
            else:
                # If not the first attribute, append a comma to the JSON string
                if (in_attributes):
                    acc_json += ','
                # Add an attribute to the JSON object
                acc_json += '"' + col + '":"' + line[col] + '"'
                in_attributes = True

        # End the attributes dictionary and the account JSON object
        acc_json += '}}'
        
        # If we have reached the limit of processed rows, trigger the API
        if (rows_processed == PROCESSED_LIMIT):
            Trigger_CDH_API('{"accounts": [' + acc_json + ']}', Token, Service_id)
            acc_json = ''
            rows_processed = 0

    # If there are remaining rows less than the processed limit, trigger the API
    if (rows_processed < PROCESSED_LIMIT):
        Trigger_CDH_API('{"accounts": [' + acc_json + ']}', Token, Service_id)