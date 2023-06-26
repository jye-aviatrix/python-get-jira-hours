# python-get-jira-hours
This python 3 script authenticate to Jira using API token, then retrieve and aggregate hours worked per day based on project ID.

# Prerequisites
- Python3
- Jira library:
    
    ```sudo pip install jira```
- credential.json
    
    Copy credential.json.sample to credential.json and modify the content to match your environment

# To generate Jira API token

- Logon to Jira
- On top right side, click on your profile picture, then choose "Manage account"

    ![Manage account](20230626095342.png)

- Security tab -> Create and manage API tokens

    ![Create and manage API tokens](20230626095548.png)

- Create API token

    ![Create API token](20230626095650.png)

- Give API token a label, eg: python-get-jira-hours

    ![Label token](20230626095802.png)

- Copy and save your API token

    ![API Token](20230626095903.png)


# To run the script
- Make sure credential.json is populated with correct information, see credential.json.sample
- Run
    ```
    python3 main.py
    ```