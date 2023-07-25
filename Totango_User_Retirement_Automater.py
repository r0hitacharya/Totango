# # Totango User Retirement Automater
# 
# This script is designed to facilitate the decommissioning of users in Totango. The primary steps include:
# 
# - Utilizes the `oauth2/api/v1/token` endpoint to acquire a temporary admin token.
# - With this token, the script interacts with the `https://api.totango.com/api/v2/scim/services/12345` SCIM service to execute the decommissioning process.
# - Efficient user management: This script can handle the deactivation of numerous user accounts simultaneously, making it especially beneficial for multinational corporations that need to manage large volumes of users.
# 
# > **Note**: The SCIM service needs to be enabled in the Totango Admin section for this script to function properly.
# 
# More about the functionality and how to manage Totango users can be found in the official [Totango documentation](https://support.totango.com/hc/en-us/articles/360021860392-Manage-Totango-users).

import datetime
import json
import requests
import warnings
import base64
warnings.filterwarnings('ignore')
from dateutil.relativedelta import relativedelta

#determine script run time
today = datetime.date.today()
print(f"Snapshot for {today}")

headers = {
    'app-token': 'ENTER YOUR TOKEN HERE',
    'ContentType': 'application/x-www-form-urlencoded'
}

# Set the base URL
base_url = 'https://app.totango.com/t01/on'

# Set the endpoint for obtaining an OAuth token
token_endpoint = f'{base_url}/oauth2/api/v1/token'

# Set the grant type
grant_type = 'client_credentials'

# Set the credentials for basic authentication
username = 'ENTER USERNAME HERE'
password = 'ENTER PASSWORD HERE'
credentials = f'{username}:{password}'
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Set the headers
headers = {'Authorization': f'Basic {encoded_credentials}'}

# Set the data for the token request
data = {'grant_type': grant_type}

# Send the token request
response = requests.post(token_endpoint, headers=headers, data=data)

# Check the response status code
if response.status_code == 200:
    # Print the response JSON
    response_json = response.json()
    access_token = response_json['access_token']
    print(f'The access token is: {access_token}')
else:
    print(f'Request failed with status code {response.status_code}')

# Set the base URL
base_url = 'https://api.totango.com/api/v2/scim/services/12345'

# Set the endpoint for updating a user
user_id = 'testing@gmail.com'
update_endpoint = f'{base_url}/Users/{user_id}'

# Set the authentication token
auth_token = access_token
headers = {'Authorization': f'Bearer {auth_token}', 'Content-Type': 'application/scim+json'}

# Set the data for the patch request, true or false will determine activation/deactivation
data = {
    'schemas': ['urn:ietf:params:scim:api:messages:2.0:PatchOp'],
    'Operations': [
        {
            'op': 'replace',
            'path': 'active',
            'value': 'false'
        }
    ]
}

# Send the patch request
response = requests.patch(update_endpoint, json=data, headers=headers)

# Check the response status code
if response.status_code == 200:
    print(f'The user {user_id} has been disabled.')
else:
    print(f'Request failed with status code {response.status_code}.')