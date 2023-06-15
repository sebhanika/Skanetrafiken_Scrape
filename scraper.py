
# Webscraper for Skanetrafiken Trafic Warnings
# Scrapes the main website of skanetrafiken to check for disruption warnings 
# and saves them in a csv file


#%% Import

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

#%% Webscrape
url = 'https://www.skanetrafiken.se'

# Send a GET request and create BeautifulSoup object 

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
div_element = soup.select_one('.urgent-traffic-info')

# Extract the text for the disruption warning
if div_element:
    div_text = div_element.get_text(strip=True)
    timestamp = datetime.now()
else:
    div_text = "No warning"
    timestamp = datetime.now()

# Read the existing CSV file that includes previous warnings
try:
    df = pd.read_csv("disruptions.csv", encoding='utf-8')
except FileNotFoundError:
    df = pd.DataFrame()

# Check if there is a new warning or if the same warning persists
if len(df) > 0:
    last_warning = df['Text'].iloc[-1]
    if last_warning == div_text:
        print("Same warning")

    else:
        print("New warning")

else:
    if div_text == "No warning":
        print("No warning")
        
    else:
        print("New warning")

#%% Write data

# Create a dictionary with the text and timestamp
data = {'Text': [div_text], 'Timestamp': [timestamp]}
disrup = pd.DataFrame(data)

# Concatenate the existing DataFrame 
df = pd.concat([df, disrup], ignore_index=True)

# Drop duplicate rows
df = df.drop_duplicates()

# Save the updated DataFrame as a CSV file
df.to_csv("disruptions.csv", index=False, encoding='utf-8')
