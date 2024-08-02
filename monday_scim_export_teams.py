"""
Script: Monday SCIM Export Teams

Description:
This script fetches team information from Monday.com using the SCIM API and exports the data to a CSV file. 
The CSV file will contain details such as Team ID, Team Name, and optionally Team Members.

Functions:
- get_monday_token: Reads the Monday.com SCIM authentication token from a specified file.
- get_scim_teams: Fetches teams and their member details from Monday.com using the SCIM API.
- write_to_csv: Writes the fetched data to a CSV file.
- main: Main function to drive the script based on user input.

Usage:
1. Run the script.
2. Enter your Monday.com domain when prompted.
3. Enter the path to your Monday.com SCIM authentication token file when prompted.
4. Choose whether to include team members in the export.
5. The script will fetch the teams and their details and export them to a CSV file named 'monday_teams.csv'.

Notes:
- Ensure that the SCIM token has the necessary permissions to access team and user details.
- Handle the SCIM token securely and do not expose it in the code.
- Customize the input prompts and error handling as needed for your organization.

Author: Chad Ramey
Date: August 2, 2024
"""

import requests
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

def get_scim_teams(auth_token, domain):
    """Fetches teams and their member details from Monday.com using the SCIM API.

    Args:
        auth_token: The Monday.com SCIM authentication token.
        domain: The Monday.com domain.

    Returns:
        A list of teams with their details.
    """
    url = f"https://{domain}.monday.com/scim/v2/Groups?scim_provisioned_only=false"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    all_teams = []
    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_teams.extend(data.get('Resources', []))

            # Handle Pagination
            total_results = data.get('totalResults', 0)
            items_per_page = data.get('itemsPerPage', 0)
            start_index = data.get('startIndex', 0)

            if start_index + items_per_page < total_results:
                url = f"https://{domain}.monday.com/scim/v2/Groups?scim_provisioned_only=false&startIndex={start_index + items_per_page}"
            else:
                url = None  # No more pages
        else:
            raise Exception(f"Error fetching teams: {response.status_code}, {response.text}")

    return all_teams

def write_to_csv(teams, include_members, filename='monday_teams.csv'):
    """Writes the fetched team data to a CSV file.

    Args:
        teams: A list of teams with their details.
        include_members: Boolean to indicate if team members should be included in the CSV.
        filename: The name of the CSV file to write to.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if include_members:
            writer.writerow(["SCIM Team ID", "Team Name", "Team Members"])
            for team in teams:
                members = '; '.join([member.get('display', '') for member in team.get('members', [])])
                writer.writerow([team.get('internalId'), team.get('displayName'), members])
        else:
            writer.writerow(["SCIM Team ID", "Team Name"])
            for team in teams:
                writer.writerow([team.get('internalId'), team.get('displayName')])

def main():
    """Main function to drive the script based on user input."""
    domain = input("Enter your monday.com domain: ")
    token_path = input("Please enter the path to your monday.com SCIM token file: ")
    auth_token = get_monday_token(token_path)
    include_members = input("Do you want to include team members in the export? (yes/no): ").strip().lower() == 'yes'
    teams = get_scim_teams(auth_token, domain)
    write_to_csv(teams, include_members)
    print(f"SCIM Teams{' and members' if include_members else ''} exported to monday_teams.csv")

if __name__ == "__main__":
    main()
