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
for i in range(28, 0, -1):
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
            
# print("")
# print("Listing daily hours")
# print("")

# # Loop through hash_table to get daily hour report
# for each_day in hash_table.keys():
#     if hash_table[each_day].keys():
#         print(each_day)
#         total_daily_seconds=0
#         for each_issue in hash_table[each_day].keys():
#             # each_issue
#             print (f"   {each_issue} {hash_table[each_day][each_issue]['description']} - {round(hash_table[each_day][each_issue]['timeSpentSeconds']/3600,2)}")
#             total_daily_seconds+=hash_table[each_day][each_issue]['timeSpentSeconds']
#         print(f"   Total daily hours: {total_daily_seconds/3600}")
#         print("")


# Get first monday of the week based on string value date
def get_first_monday_of_week(date_string):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    # Find the weekday of the date (Monday is 0 and Sunday is 6)
    weekday = date_obj.weekday()
    # Calculate the Monday of the first week
    monday_first_week = date_obj - timedelta(days=weekday)
    return(monday_first_week.strftime('%Y-%m-%d'))


# Get the range from the first Monday to the following Sunday
def get_week_range(date_string):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()    
    # Find the weekday of the date (Monday is 0 and Sunday is 6)
    weekday = date_obj.weekday()    
    # Calculate the Monday of the first week
    monday_first_week = date_obj - timedelta(days=weekday)    
    # Calculate the Sunday of the same week
    sunday_first_week = monday_first_week + timedelta(days=6)    
    # Format the result as a string
    range_string = f"{monday_first_week.strftime('%Y-%m-%d')} to {sunday_first_week.strftime('%Y-%m-%d')}"    
    return range_string

# Get the name of the day of the week, returns Monday, Tuesday ... Sunday
def day_name(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
    day_name = date_obj.strftime("%A")
    return day_name


weekly_hours={}

# Loop through hash_table to get seconds of each week aggregated by first Monday of the week.
for each_day in hash_table.keys():
    first_monday_of_week=get_first_monday_of_week(each_day)
    for each_issue in hash_table[each_day].keys():
        if first_monday_of_week in weekly_hours.keys():
            weekly_hours[first_monday_of_week]['weeklySeconds']+=hash_table[each_day][each_issue]['timeSpentSeconds']
        else:
            weekly_hours[first_monday_of_week]={}
            weekly_hours[first_monday_of_week]['weeklySeconds']=hash_table[each_day][each_issue]['timeSpentSeconds']

# # Print out weekly hours by first Monday of the week
# print("")
# print("Listing weekly hours")
# print("")
# for each_monday in weekly_hours.keys():
#     print(f"First Monday of the week: {each_monday} hours logged: {round(weekly_hours[each_monday]['weeklySeconds']/3600,2)}. This is {round(weekly_hours[each_monday]['weeklySeconds']/1440,2)}% of 40 hours week")


# Print out weekly and daily report combined
for each_monday in weekly_hours.keys():
    print("------------------------------------------------------")
    print(f"Week of: {get_week_range(each_monday)}")
    print(f"Hours logged: {round(weekly_hours[each_monday]['weeklySeconds']/3600,2)}. This is {round(weekly_hours[each_monday]['weeklySeconds']/1440,2)}% of 40 hours week")
    print("------------------------------------------------------")
    for each_day in hash_table.keys():
        if hash_table[each_day].keys() and each_monday==get_first_monday_of_week(each_day):
            print(f"{each_day} {day_name(each_day)}")
            total_daily_seconds=0
            for each_issue in hash_table[each_day].keys():
                # each_issue
                print (f"   {each_issue} {hash_table[each_day][each_issue]['description']} - {round(hash_table[each_day][each_issue]['timeSpentSeconds']/3600,2)}")
                total_daily_seconds+=hash_table[each_day][each_issue]['timeSpentSeconds']
            print(f"   Total daily hours: {round(total_daily_seconds/3600,2)}")
            print("")
