# Totango
A guide to Totango (Client Success Platform) API calls, demonstrating usage, responses, and integration strategies. Covers everything from authentication to event triggers. Ideal for developers leveraging Totango's functionalities

## List

:bookmark: **Totango User List :** 

This script fetches user data from the Totango API in a paginated manner, cleans the data and finally consolidates the data into a DataFrame for further analysis or usage.

:bookmark: **Totango Audit Log API Call :** 

This script interacts with the Totango Audit Log API. It fetches user adoption data based on a specified date range (start and end dates), cleans the received data, and finally consolidates it into a DataFrame for further analysis or usage. The script is easily customizable allowing for data retrieval for any given time period, making it a versatile tool for user adoption data analysis.

:bookmark: **Totango_API_CSV_Data_Integration :**

This script automates the process of uploading data to Totango from a CSV file by triggering an API endpoint. It allows immediate data upload to Totango post data-preparation, thereby increasing efficiency and reducing manual work. 

:bookmark: **Automated Extraction of SuccessPlay Stats via API :**

This script is designed to automate the extraction of SuccessPlay statistics from Totango, utilizing the tasks/export API. The key feature is the conversion of manual data extraction process from the UI into an automated script-based approach.

:bookmark: **Totango_SFTP_Joblog_API :**

This script extracts detailed information on the integrations of all SFTP and non-SFTP data jobs running on Totango. It aids in building a dashboard to monitor daily load statuses and triggers remedial actions in case of job failures.

:bookmark: **Totango Touchpoints API:**

This script is designed to interact with the [Touchpoints API](https://support.totango.com/hc/en-us/articles/115000597266-Touchpoints-API) and aims to backup all touchpoints, notes, and alerts for all clients in a systematic and automated way. It forms a critical part of a broader monitoring system and is essential in facilitating data analysis and insights.

:bookmark: **Totango Attribute Modifier :**

This script is a tool for efficient and precise modification of attributes in Totango. It defines a JSON structure detailing the attributes to be modified for a specified ID, typically a client ID in Totango. Utilizing the Totango Account API from the Integration Hub, the script updates the user attributes and returns a batch ID for reference and verification.


