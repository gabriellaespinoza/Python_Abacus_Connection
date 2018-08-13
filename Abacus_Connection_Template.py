import os
import csv
import json
import requests
from dotenv import load_dotenv

load_dotenv('/Users/location_of_env_file/creds.env') # fill this in
print(os.environ['ABACUS_USERNAME']) 
print(os.environ['ABACUS_PASSWORD']) 

def get_abacus_sql(client, query):
    '''
    Parameters:
        client - the client slug for the request query
        query - the string of sql that you want to execute
    Returns: a csv reader object on the request
    '''

    url = "https://abacus.bluestatedigital.com/export/api/sql/{}".format(client)

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

    headers = {"Content-Type": "application/json"}
    auth = (os.environ['ABACUS_USERNAME'], os.environ['ABACUS_PASSWORD'])

    # Step 1: make the post request to have abacus generate the file
    csv_url_request = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))

    print(csv_url_request.status_code)
    print(csv_url_request.ok)
    print(csv_url_request.text)
    print(csv_url_request.json())

    # Step 2: Retrieve the file location
    results_request = requests.get(csv_url_request.json()['resultBody'], auth=auth, headers=headers)

    reader = csv.DictReader(results_request.content.decode('utf-8').splitlines(), delimiter=',', quotechar='"')

    return reader

my_client = "insert_slug" # fill this in
my_query = """insert_query""" # fill this in

get_abacus_sql(my_client, my_query)