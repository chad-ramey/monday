"""
Script: Monday Export Users with Proper User ID

Description:
This script fetches user information from Monday.com using the SCIM API and exports the data to a CSV file. 
The CSV file will contain details such as User ID and other relevant fields fetched from the API.

Functions:
- get_monday_token: Reads the Monday.com authentication token from a specified file.
- main: Main function to fetch and export user data based on user input.

Usage:
1. Run the script.
2. Enter the path to your Monday.com API token file when prompted.
3. The script will fetch the user details and export them to a CSV file named 'users.csv'.

Notes:
- Ensure that the API token has the necessary permissions to access user details.
- Handle the API token securely and do not expose it in the code.
- Customize the input prompts and error handling as needed for your organization.

Author: Chad Ramey
Date: August 2, 2024
"""

import requests
import json
import csv

def get_monday_token(token_path):
    """Reads the Monday.com authentication token from a specified file.

    Args:
        token_path: The path to the file containing the Monday.com token.

    Returns:
        The Monday.com token as a string.
    """
    with open(token_path, 'r') as token_file:
        return token_file.read().strip()

def main():
    """Main function to fetch and export user data based on user input."""
    # Prompt the user for the path to their API token file
    token_path = input("Please enter the path to your API token file: ")
    access_token = get_monday_token(token_path)

    # Define your API endpoint and headers
    url = "https://onepeloton.monday.com/scim/v2/Users"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    # Initialize an empty list to store all the data
    all_users = []

    # Loop through the paginated results
    start_index = 1
    items_per_page = 50

    while True:
        params = {
            'itemsPerPage': items_per_page,
            'startIndex': start_index
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            resources = data.get('Resources', [])

            # Add the fetched users to the list
            all_users.extend(resources)

            # Check for pagination
            total_results = data.get('totalResults', 0)
            start_index += items_per_page

            if start_index > total_results:
                break
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            break

    # Save the data to a CSV file
    csv_file = 'users.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_users[0].keys())

        # Write header
        writer.writeheader()

        # Write data
        writer.writerows(all_users)

    print(f"Data exported to {csv_file}")

if __name__ == "__main__":
    main()
