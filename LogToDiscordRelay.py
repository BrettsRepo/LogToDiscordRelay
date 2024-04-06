########################################################### 
###########################################################
####### LogToDiscordRelay.py Chalkdust p99green 2023Sept01
###########################################################
###########################################################
## PURPOSE: Monitors (EverQuest) log file and sends a message in Discord  when trigger text is found.
########################################################### 
###########################################################
## SETUP INSTRUCTIONS
## STEP 1. Save this as a '.py' file in a known location on your computer
## STEP 2. Install python on your computer
## STEP 3. Create a personal Discord server and setup a Channel, name them whatever you like as long as you are Admin on the server
## STEP 4. In Discord right click Channel > Edit Channel > Integrations > Webhooks
## STEP 5. New Webhook > Name it whatever you like > Copy Webhook URL
## STEP 6. Edit the line of code below which shows: webhook_url = 'https://discord...' and paste your correct webhook url (surrounded by single quotes)
## STEP 7. Edit the line of code below which shows: log_file_path = 'c:\p99_nNew\Logs...' and replace with your log file location
## STEP 8. Adjust and add any desired trigger text matches
## STEP 9. Save your changes
###########################################################
########################################################### 
## USAGE INSTRUCTIONS
## STEP 1. Navigate to the folder where you saved this file
## STEP 2. In the folder address bar type CMD and click Enter to launch Command Promp (with path set to this folder location)
## STEP 3. input the following text and click enter: python LogToDiscordRelay.py 
## STEP 4. Test by logging into your character with the selected log file and /say trigger text and check your discord channel for the relayed message
###########################################################
########################################################### 
## MODIFICATION: If not Python friendly, provide the code to ChatGPT and ask for your changes, give it a shot
###########################################################
###########################################################

import os
import time
import requests
import re

# Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/REPLACE_ALL_WITH_YOUR_WEBHOOK_URL'

# Log file path
log_file_path = 'C:\p99_New\Logs\eqlog_Chalkdust_P1999Green.txt.REPLACE_ALL_WITH_YOUR_LOG_FILE_PATH_LOCATION'

# List of regular expression patterns for trigger texts
# Update using regex to include additional trigger texts as shown below
trigger_patterns = [
    r'YOU for (.+) damage',
    r'you for (.+) points of damage',
    r'->',
    r'tells you',
    r'AnotherPattern (.+) something else'
]

# Initialize the last checked position in the log file
last_position = 0

while True:
    try:
        with open(log_file_path, 'r') as f:
            # Move to the last checked position
            f.seek(last_position)

            # Read new lines
            new_lines = f.readlines()
            last_position = f.tell()

            # Find the most recent line that matches any trigger pattern
            recent_line = None
            for line in reversed(new_lines):
                for trigger_pattern in trigger_patterns:
                    match = re.search(trigger_pattern, line)
                    if match:
                        recent_line = line.strip()
                        print('Found matching line:', recent_line)  # Print matching line
                        break
                if recent_line:
                    break

            # Send notification to Discord for the most recent matching line
            if recent_line:
                payload = {'content': recent_line}
                response = requests.post(webhook_url, json=payload)
                if response.status_code != 204:
                    print('Failed to send notification to Discord.')

    except Exception as e:
        print('An error occurred:', str(e))  # Print any exceptions
   
    # Wait before checking for new changes
    time.sleep(.1)  # Adjust the interval as needed, checking every 100ms by default