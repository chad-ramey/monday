# Monday.com Lab

This repository contains Python scripts designed to automate tasks related to managing Monday.com users, teams, and SCIM exports.

## Table of Contents
  - [Table of Contents](#table-of-contents)
  - [Scripts Overview](#scripts-overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Scripts Overview
Here’s a list of all the scripts in this repository along with their descriptions:

1. **monday_batch_userType.py**: Automates the batch processing of user types in Monday.com, such as assigning or modifying user roles in bulk.
2. **monday_export_users.py**: Exports a list of users from Monday.com, including their details for reporting and administrative purposes.
3. **monday_scim_export_teams.py**: Exports team data using SCIM integration, allowing for team management and updates.
4. **monday_team_membership.py**: Manages team memberships in Monday.com, including adding or removing users from teams.

## Requirements
- **Python 3.x**: Ensure that Python 3 is installed on your system.
- **Monday.com API**: Install the required libraries to interact with the Monday.com API.
- **API Keys**: You will need Monday.com API tokens to authenticate API requests.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/monday-automation-scripts.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Monday.com API tokens and other necessary credentials in environment variables:
   ```bash
   export MONDAY_API_TOKEN="your-token-here"
   ```

## Usage
Run the desired script from the command line or integrate it into your Monday.com workflows.

Example:
```bash
python3 monday_export_users.py
```

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the functionality or add new features.

## License
This project is licensed under the MIT License.
