from jira import JIRA
from datetime import datetime, timedelta
import json

# Read the JSON file
with open('credential.json', 'r') as file:
    data = json.load(file)

# Jira account credentials
JIRA_USERNAME = data['JIRA_USERNAME']
JIRA_API_TOKEN = data['JIRA_API_TOKEN']

# Jira server information
JIRA_SERVER = data['JIRA_SERVER']
JIRA_QUERY = data['JIRA_QUERY']



# Create a JIRA object with API token authentication
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

# Example: Retrieve and print the currently logged-in user
user = jira.myself()
print(f"Logged-in User: {user['displayName']} ({user['emailAddress']})")



# Get the current date
current_date = datetime.now().date()

# Create a blank hash table
hash_table = {}

# Pre-populate the hash table with date as key of the last four weeks
for i in range(1, 29):
    # Calculate the date for the current iteration
    date = current_date - timedelta(days=i)
    
    # Use the date as the key in the hash table
    hash_table[date.strftime('%Y-%m-%d')] = {}


# Hash table structure
# '2023-06-25'
#	|_ 'ACS_2663'
#		|_ 'description'
#		|_ 'timeSpentSeconds'
#

# Query against Jira, where it's ACS project, unresolved and assigned to current user

# Get list of issues based on the query
issues = jira.search_issues(JIRA_QUERY)

# Loop through each issue
for issue in issues:
    print(f'working on issue: {issue.key} {issue.fields.summary}')
    worklogs = jira.worklogs(issue.key)
    for worklog in worklogs:
        worklog_date = datetime.strptime(worklog.started, '%Y-%m-%dT%H:%M:%S.%f%z').date().strftime('%Y-%m-%d')
        worklog_seconds = worklog.timeSpentSeconds
        # print(f"started: {worklog_date}")
        # print(f"timeSpentSeconds: {worklog_seconds}")
        if worklog_date in hash_table.keys():
            if issue.key in hash_table[worklog_date].keys():
                hash_table[worklog_date][issue.key]['timeSpentSeconds']+=worklog_seconds
            else:
                hash_table[worklog_date][issue.key]={}
                hash_table[worklog_date][issue.key]['timeSpentSeconds']=worklog_seconds
                hash_table[worklog_date][issue.key]['description']=issue.fields.summary
            
print("")
print("Listing daily hours")
print("")
# Loop through hash_table
for each_day in hash_table.keys():
    if hash_table[each_day].keys():
        print(each_day)
        total_daily_seconds=0
        for each_issue in hash_table[each_day].keys():
            # each_issue
            print (f"   {each_issue} {hash_table[each_day][each_issue]['description']} {hash_table[each_day][each_issue]['timeSpentSeconds']/3600}")
            total_daily_seconds+=hash_table[each_day][each_issue]['timeSpentSeconds']
        print(f"   Total daily hours: {total_daily_seconds/3600}")
        print("")