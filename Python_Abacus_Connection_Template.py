# Import necessary modules
import os
import csv
import json
import requests
from dotenv import load_dotenv
import webbrowser
import time
import pandas as pd

# Load environment variables(Abacus username and password) from .env file
load_dotenv('/Users/FolderName/creds.env')  # Fill this in with path to your directory and name of .env file
print(os.environ['ABACUS_USERNAME'])
print(os.environ['ABACUS_PASSWORD'])

# Define function with parameters
def get_abacus_sql(client, query):
    '''
    Parameters:
        client - the client slug for the request query
        query - the string of sql that you want to execute
    Returns: a csv reader object on the request
    '''

# Use API to communicate with sql on Abacus and create url with client slug at the end
    url = "https://abacus.bluestatedigital.com/export/api/sql/{}".format(client)

# Create dictionaries to select the same settings as Abacus for running query and outputting a csv file
    payload = {
        "clients": [client],
        "customFields": {},
        "exportSettings": {
            "format": {
                "name": "csv",
                        "opts": {
                            "delimiter": ",",
                            "headerRow": True,
                            "extension": "csv"
                        },
            },
            "extra": {"zip_file": {"value": False}, "email": {"recipients": []}},
            "export": {"name": "file", "opts": {"fileslug": "", "timestamp": True}}},
        "twigSQL": query,
    }

# Use json to transmit data between (Abacus or python?) and .env file # unsure about this one
    headers = {"Content-Type": "application/json"}
    auth = (os.environ['ABACUS_USERNAME'], os.environ['ABACUS_PASSWORD'])

# Steps for creating csv file
    # Step 1: make the post request to have Abacus generate the file
    global csv_url_request
    csv_url_request = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))
    print(type(csv_url_request))
    print(csv_url_request.status_code)
    print(csv_url_request.ok)
    print(csv_url_request.text)
    print(csv_url_request.json())

    # Step 2: Retrieve the file location
    results_request = requests.get(csv_url_request.json()['resultBody'], auth=auth, headers=headers)

    reader = csv.DictReader(results_request.content.decode('utf-8').splitlines(), delimiter=',', quotechar='"')

    return reader

# Input client slug and query
my_client = "insert_slug"  # Fill this in
my_query = """insert_query"""  # Fill this in

get_abacus_sql(my_client, my_query)

# Call result body and use webbroswer to open and download link for csv online
full_link = csv_url_request.json()['resultBody']
web_open = webbrowser.open(full_link)
time.sleep(5)

# Split string and take end of link to get the name of actual file downloaded
split_link = str(full_link).split('/')[-1]
print(split_link)

# Open csv file from folder it was downloaded in
dir = "/Users/FolderName/Downloads"  # Add in your directory and file path that csv was downloaded in(will most \
# likely be Downloads)
os.chdir(dir)

# Combine directory with ending of link for csv name
my_file = str('/Users/FolderName/Downloads/' + split_link)

# Create pandas data frame to open and read csv file in Python
my_df = pd.read_csv(my_file)
print(my_df.head(5))  # Print first 5 rows

# Do a bunch of transformations!

"""

To have your file open in user directory
output_file = "/Users/FolderName/user_folder_output.csv"
my_df.to_csv(output_file)
os.remove(my_file)

"""
