"""
Script: Export Monday.com Teams to CSV

Description:
This script fetches team information from Monday.com using the Monday.com API and exports the data to a CSV file. 
The CSV file will contain details such as Team ID, Team Name, Picture URL, User ID, User Name, User Email, User Created At, and User Phone.

Functions:
- get_monday_token: Reads the Monday.com authentication token from a specified file.
- get_teams: Fetches teams and their user details from Monday.com.
- write_to_csv: Writes the fetched data to a CSV file.
- main: Main function to drive the script based on user input.

Usage:
1. Run the script.
2. Enter the path to your Monday.com authentication token file when prompted.
3. The script will fetch the teams and their details and export them to a CSV file named 'monday_standard_teams.csv'.

Notes:
- Ensure that the Monday.com authentication token has the necessary permissions to access team and user details.
- Handle the authentication token securely and do not expose it in the code.
- Customize the input prompts and error handling as needed for your organization.

Author: Chad Ramey
Date: August 2, 2024
"""

import requests
import csv
import json

def get_monday_token(token_path):
    """Reads the Monday.com authentication token from a specified file.

    Args:
        token_path: The path to the file containing the Monday.com token.

    Returns:
        The Monday.com token as a string.
    """
    with open(token_path, 'r') as token_file:
        return token_file.read().strip()

def get_teams(auth_token):
    """Fetches teams and their user details from Monday.com.

    Args:
        auth_token: The Monday.com authentication token.

    Returns:
        A list of teams with their details.
    """
    url = "https://api.monday.com/v2/"
    payload = {
        "query": "query { teams { id name picture_url users { id name email created_at phone } } }"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return json.loads(response.text)['data']['teams']
    else:
        raise Exception(f"Error fetching teams: {response.status_code}, {response.text}")

def write_to_csv(teams, filename='monday_standard_teams.csv'):
    """Writes the fetched team data to a CSV file.

    Args:
        teams: A list of teams with their details.
        filename: The name of the CSV file to write to.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Team ID", "Team Name", "Picture URL", "User ID", "User Name", "User Email", "User Created At", "User Phone"])

        for team in teams:
            for user in team.get('users', []):
                writer.writerow([
                    team.get('id'), team.get('name'), team.get('picture_url'),
                    user.get('id'), user.get('name'), user.get('email'), user.get('created_at'), user.get('phone')
                ])

def main():
    """Main function to drive the script based on user input."""
    token_path = input("Please enter the path to your monday.com auth token file: ")
    auth_token = get_monday_token(token_path)
    teams = get_teams(auth_token)
    write_to_csv(teams)
    print("Standard API Teams exported to monday_standard_teams.csv")

if __name__ == "__main__":
    main()
