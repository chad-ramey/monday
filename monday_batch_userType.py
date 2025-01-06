"""
Script: Monday Batch Update User Type

Description:
This script batch updates the user type of multiple users on Monday.com using the SCIM API. 
It reads user IDs from a specified CSV file and updates each user to the 'viewer' user type.

Functions:
- get_monday_token: Reads the Monday.com SCIM authentication token from a specified file.
- main: Main function to perform the batch update based on user input.

Usage:
1. Run the script.
2. Enter the path to your Monday.com API token file when prompted.
3. Enter the path to your CSV file containing user IDs when prompted.
4. The script will update the user type of each user ID listed in the CSV file.

Notes:
- Ensure that the API token has the necessary permissions to update user details.
- Handle the API token securely and do not expose it in the code.
- Customize the input prompts and error handling as needed for your organization.
- CSV header is user_ids followed by list of Monday account IDs 

Author: Chad Ramey
Date: January 6, 2025
"""

import requests
import json
import csv

def get_monday_token(token_path):
    """Reads the Monday.com SCIM authentication token from a specified file.

    Args:
        token_path: The path to the file containing the Monday.com token.

    Returns:
        The Monday.com token as a string.
    """
    with open(token_path, 'r') as token_file:
        return token_file.read().strip()

def main():
    """Main function to perform the batch update based on user input."""
    # Prompt the user for the path to their API token file
    token_path = input("Please enter the path to your API token file: ")
    api_key = get_monday_token(token_path)

    # Define the base URL
    base_url = 'https://onepeloton.monday.com/scim/v2/Users/'

    # Prompt the user for the CSV file location
    csv_file_location = input("Enter the path to the CSV file (e.g., user_ids.csv): ")

    # Open the CSV file and read user IDs
    try:
        with open(csv_file_location, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user_id = row['user_id']
                url = base_url + user_id

                payload = {
                    "schemas": [
                        "urn:ietf:params:scim:api:messages:2.0:PatchOp"
                    ],
                    "Operations": [
                        {
                            "op": "replace",
                            "value": {
                                "userType": "viewer"
                            }
                        }
                    ]
                }

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }

                response = requests.patch(url, headers=headers, json=payload)

                if response.status_code == 200:
                    print(f"User {user_id} updated successfully.")
                else:
                    print(f"Error updating user {user_id}: {response.status_code} - {response.text}")
    except FileNotFoundError:
        print("CSV file not found. Please provide a valid file location.")

if __name__ == "__main__":
    main()
