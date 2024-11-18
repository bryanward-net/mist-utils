#!/usr/bin/env python3
import requests

# Created by Bryan Ward, www.bryanward.net
# Released under the MIT License.  See included LICENSE file for information.

# Define values that are specific to your environment.
# Info on how to create an API Token and the
# URLs for Mist Cloud Regions are defined here:
# https://www.juniper.net/documentation/us/en/software/mist/automation-integration/topics/topic-map/api-endpoint-url-global-regions.html

MIST_URL = "https://api.mist.com/api/v1"
MIST_ORG_ID = "00000000-1111-2222-3333-444444444444"
MIST_API_TOKEN = "YOUR-API-TOKEN-HERE"


# Fetch all sites in the given organization
response = requests.get(MIST_URL + f"/orgs/{MIST_ORG_ID}/sites", headers={"Authorization": f"Token {MIST_API_TOKEN}"})

if response.status_code == 200:
    # 200 means OK.  Anything else indicates an error.
    sites = response.json()
elif response.status_code == 401:
    raise Exception("Unauthorized.  Authentication credentials were not provided.  Check that you provided a valid API Token.")
elif response.status_code == 403:
    raise Exception("Permission Denied.  You do not have permission to perform this action.  Check that your API Token has read/write permissions.")
elif response.status_code == 404:
    raise Exception("Not Found.  The API endpoint doesn't exist or resource doesn' t exist.  Check that you speficied the correct URL for your region and ORG ID.")
elif response.status_code == 429:
    raise Exception("Too Many Requests.  The API Token used for the request reached the 5000 API Calls per hour threshold.  Try again later.")
else:
    # Some other error code was returned
    raise Exception(response.text)


# Step thru each site in the organization
for site in sites:
    print(f"Checking site {site['name'] or site['id']}...")
    # Fetch all devices in the site
    devices = requests.get(MIST_URL + f"/sites/{site['id']}/devices", headers={"Authorization": f"Token {MIST_API_TOKEN}"}).json()
    for device in devices:
        if "locating" in device and device['locating']:
            print(f"Disabling Locate LED on device {device['name'] or device['mac']}...", end="")
            # Send config to disable the Locate LED
            response = requests.put(MIST_URL + f"/sites/{site['id']}/devices/{device['id']}", headers={"Authorization": f"Token {MIST_API_TOKEN}"}, json={"locating": False})
            if response.status_code == 200: # 200 means OK
                print("Success!")
            elif response.status_code == 403:
                raise Exception("Permission Denied.  You do not have permission to perform this action.  Check that your API Token has write permissions.")
            elif response.status_code == 429:
                raise Exception("Too Many Requests.  The API Token used for the request reached the 5000 API Calls per hour threshold.  Try again later.")
            else:
                # Some other error code was returned
                raise Exception(response.text)


print("Done!")
