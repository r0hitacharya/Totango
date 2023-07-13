# # Totango Attribute Modifier 
# 
# The `Totango_Attribute_Modifier` is a script aimed at providing a streamlined method of updating attributes for a given ID, often the client ID, in Totango. It leverages the capabilities of Totango's Account API provided in the [Integration Hub](https://int-hub.totango.com/) to perform these operations.
# 
# ## Highlights
# 
# - The script prepares a JSON-formatted body that lists the various attributes to be modified for a particular ID.
# - By making a call to the Totango Account API, the script initiates the attribute update process.
# - Once the attribute update process is complete, the script retrieves the corresponding batch ID, which can be used for tracking or reference purposes in the future.
# - This tool significantly simplifies attribute management in Totango, enabling users to effortlessly keep their data current and accurate.
# 

# # Libraries

import json
import requests
from datetime import datetime


# # Call

#the autherization token needs to be obtained from totango and passed in the header
headers = {
    'content-type' : 'application/json',
    'Authorization': 'PUT YOUR TOKEN HERE',
    'service_id' : 'GET THE SERVICE ID FROM TOTANGO UI'
}


body = {
    "accounts": [{
        "id": "Your ClientID",
        "attributes": {
            "SFDC_Segment": "Large Cap Account",
            "Success Manager": "Mr Coder"
        }
    }]
}


response = requests.post(
    'https://int-hub.totango.com/api/v1/accounts', headers=headers, json=body)

content = json.loads(response.content)
status = content.get('status')
time_received = content.get('time_received')

if status == 'success':
    # Separating date and time
    dt_object = datetime.strptime(time_received, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = dt_object.date()
    time = dt_object.time()
    print("The attribute was changed successfully on date {} at time {} (24-hour format).".format(date, time))
    print("Batch ID returned by the API:",batch_id)
else:
    print("The attribute was not changed successfully please rerun/debug the script")