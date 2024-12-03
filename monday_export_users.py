"""
Script: Monday Export Users with Last Activity

Description:
This script fetches user information from Monday.com using the GraphQL API and exports the data to a CSV file.
The CSV file will contain details such as User ID, Name, Email, Created At, and Last Activity.

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

Author: Chad Ramey
Date: December 3, 2024
"""

import requests
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
    url = "https://onepeloton.monday.com/v2"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    # GraphQL query to fetch user details, including last activity
    query = """
    {
        users {
            id
            name
            email
            created_at
            last_activity
        }
    }
    """

    # Make the API request
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json()

        # Check for errors in the response
        if 'errors' in data:
            print(f"Error in response: {data['errors']}")
            return

        # Extract user data
        users = data['data']['users']

        # Save the data to a CSV file
        csv_file = 'users.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'email', 'created_at', 'last_activity'])
            writer.writeheader()
            writer.writerows(users)

        print(f"Data exported to {csv_file}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response content: {response.text}")

if __name__ == "__main__":
    main()
