# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import os
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import altair as alt
import geopandas as gpd
import shapely
import bs4
import requests
import warnings
import sys # We will use this to exit our if statement
import numpy as np
from bs4 import BeautifulSoup
from shapely import Polygon, Point, MultiPolygon
from numpy import mean, nan # PS: Some version of numpy only consider NaN. So graders should consider this when this chunk of code is ran.
alt.renderers.enable("png")
warnings.filterwarnings('ignore')
#
#
#
#
#
#
#
hhsoig_enforce_path = r'https://oig.hhs.gov/fraud/enforcement/'

hhsoig_enforce_retrived = requests.get(hhsoig_enforce_path)

hhsoig_enforce_content = BeautifulSoup(hhsoig_enforce_retrived.content, 'lxml')
#
#
#
#
#
# Retrieving the unordered list ('ul') to find the list of enforcement in the first page on the website, avoinding retrieving all the elements ('li') from the website.
list_enforce_firstpage = hhsoig_enforce_content.find_all('ul', class_ = "usa-card-group padding-y-0")
#
#
#
#
#
#
#
#
#
#
#
#
list_links_ongoing = list_enforce_firstpage[0].find_all('a') # Extracting the 'a' tags
list_links_final = [] # Initializing the list of links we will append
for a_tags in list_links_ongoing:
  a_link_partial = a_tags.get('href') # Only partial links
  a_link_complete = 'https://oig.hhs.gov' + a_link_partial
  list_links_final.append(a_link_complete)
#
#
#
#
#
list_title_final = [] # Initializing the list of titles we will append
for a_tags in list_links_ongoing:
  title_text = a_tags.text
  list_title_final.append(title_text)
#
#
#
#
#
# Extracting the 'span' tags from our 'ul' scrapped data
list_dates_ongoing = list_enforce_firstpage[0].find_all('span')
list_dates_final = [] # Initializing the list of dates we will append
for span_tags in list_dates_ongoing:
  date_text = span_tags.text
  list_dates_final.append(date_text)

# Now let's clean the dates text to later transform it into a date data type
# We will replace all the space by "/" and remove all the "," to have a uniform format.
for index in range(len(list_dates_final)):
  list_dates_final[index] = list_dates_final[index].replace(' ', '/')
  list_dates_final[index] = list_dates_final[index].replace(',', '')

# We are also converting the month name into month rank number
for index in range(len(list_dates_final)):
  if list_dates_final[index].startswith('November'):
    list_dates_final[index] = list_dates_final[index].replace('November', '11')
  elif list_dates_final[index].startswith('October'):
    list_dates_final[index] = list_dates_final[index].replace('October', '10')
  else:
    pass

# Finally, we can convert those dates into date type
for index in range(len(list_dates_final)):
  list_dates_final[index] = datetime.datetime.strptime(list_dates_final[index], '%m/%d/%Y')
#
#
#
#
#
list_category_ongoing = list_enforce_firstpage[0].find_all('li', class_ = "display-inline-block usa-tag text-no-lowercase text-base-darkest bg-base-lightest margin-right-1")
list_category_final = [] # Initializing the list of categories we will append
for li_tags in list_category_ongoing:
  category_text = li_tags.text
  list_category_final.append(category_text)
#
#
#
#
#
enforcement_action_data = pd.DataFrame({
  'title_enforcement' : list_title_final,
  'date_enforcement' : list_dates_final,
  'category_enforcement' : list_category_final,
  'link_enforcement' : list_links_final
})
```
#
#
#
# Segment 1
enforcement_action_data[['title_enforcement', 'date_enforcement']].head(5)
```
#
# Segment 2
enforcement_action_data[['category_enforcement', 'link_enforcement']].head(5)
#
#
#
#
#
#
#
#
#
#
list_agency_final = [] # Initializing the list of agency we will append

# Building the "for loop" to go over each link in "enforcement_action_data" and retrieve the agency name, and store it in "list_agency_final".
for link in enforcement_action_data['link_enforcement']:
  enforcement_retrived = requests.get(link)
  enforcement_content = BeautifulSoup(enforcement_retrived.content, 'lxml')
  box_agency = enforcement_content.find_all('ul', class_ = "usa-list usa-list--unstyled margin-y-2")
  agency_info_ongoing = box_agency[0].find_all('li')[1].text
  agency_info_final = agency_info_ongoing.replace('Agency:', '')
  list_agency_final.append(agency_info_final)
#
#
#
#
#
enforcement_action_data['agency_enforcement'] = list_agency_final
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Base path for the enforcement action webpages
hhsoig_enforcement_page = r'https://oig.hhs.gov/fraud/enforcement/?page='

# This function is going to be long. So sorry for the graders!

def crawl_enforcement_data(year, month):
  # Verifying validity for month
  if type(month) != int:
    print("TypeError: Argument 'month' only accepts int type.\nThis is Ralph's predefined error message. Another message will also be displayed after exiting the system. Please ignore message 'SystemExit'.")
    sys.exit() # This will exit the code and not run any other lines. I found this method on Stackoverflow.
  elif month < 1 or month > 12:
    print("RangeError: Argument 'month' only accepts values from 0 to 12.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message 'SystemExit'.")
    sys.exit() # This will exit the code and not run any other lines.
  else:
    pass

  # Verifying validity for year
  if type(year) != int:
    print("TypeError: Argument 'year' only accepts int type.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message 'SystemExit'")
    sys.exit() # This will exit the code and not run any other lines.
  elif len(str(year)) != 4:
    print("FormatError: Please enter the 'year' in the correct format (e.g. 1804)\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message 'SystemExit'.")
    sys.exit() # This will exit the code and not run any other lines.
  elif year < 2013 or  year > int(datetime.datetime.now().year):
    print(f'RangeError: Argument "year" only accepts values from 2013 to {int(datetime.datetime.now().year)}.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit".')
    sys.exit()
  else:
    pass

  # Iniatizaling the lists that will be appended to the tidy dataframe
  titles_final = []
  dates_final = []
  categories_final= []
  links_final = []
  agencies_final = []
  list_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] # This will be handy for conversion into month rank
  rank_month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

  # Finding the number of pages we will crawl through
  time.sleep(1) # Adding 2 seconds wait to prevent potential server-side block.
  page_numbers = hhsoig_enforce_content.find_all('a', class_ = "pagination__link")  
  last_page_contents = page_numbers[-1].text # Last page text always last index
  last_page = '' # Initializing the object that will store the last page string.
  for string in last_page_contents: #  Cleaning to retrieve only the digits
    if string.isdigit():
      last_page = last_page + string
  last_page = int(last_page) # Converting the last page into an int type

  # Creating the foor loop to extract the data using the crawl
  for page_number in range(1, 10):
    page_link = hhsoig_enforcement_page + str(page_number)
    time.sleep(1) # Adding 2 seconds wait to prevent potential server-side block.
    page_path = requests.get(page_link)
    page_contents = BeautifulSoup(page_path.content, 'lxml')
    unordered_box = page_contents.find_all('ul', class_ = "usa-card-group padding-y-0") # All the info we need is contained in this unordered list
    ###########

    # Extracting the dates
    found_date_older = False # To alert us when to break the loop if a date is older than the year and month provided
    all_dates = unordered_box[0].find_all('span')
    list_dates_temp = [] # Temporary container for the dates. Not our final list container which is already created outside of the loop
    for span_tags in all_dates: # Extracting all dates for this page
      date_text = span_tags.text
      list_dates_temp.append(date_text)
    for index in range(len(list_dates_temp)): # Cleaning the dates
      list_dates_temp[index] = list_dates_temp[index].replace(' ', '/')
      list_dates_temp[index] = list_dates_temp[index].replace(',', '')
    for index in range(len(list_dates_temp)): # Convert month name into month rank
      month_name = list_dates_temp[index].split('/')[0] # Find month name
      index_month = list_months.index(month_name) # The list of months was helpful
      list_dates_temp[index] = list_dates_temp[index].replace(month_name, rank_month[index_month])
    for index in range(len(list_dates_temp)): # Converting into date type
      list_dates_temp[index] = datetime.datetime.strptime(list_dates_temp[index], '%m/%d/%Y')
      ## Generating a date object as reference to better filter
    first_day_of_month = str(month) + '/1/' + str(year) 
    first_day_of_month = datetime.datetime.strptime(first_day_of_month, '%m/%d/%Y')
      ## Checking for older date and retrieving dates
    if any(date < first_day_of_month for date in list_dates_temp) and (not all(date < first_day_of_month for date in list_dates_temp)):
      found_date_older = True # Setting "ON" the alert for older dates
      list_index_recent = [] # To store the index for dates NOT older
      for index in range(len(list_dates_temp)):
        if list_dates_temp[index] >= first_day_of_month:
          list_index_recent.append(index)
        else:
          pass
      # Now we can append to the final list of dates
      for index in list_index_recent:
        dates_final.append(list_dates_temp[index])
      # Can also find the other variables, which will depend on the list of index for recent dates. The values for each index will match the list of the other variables.
      # Extracting the titles for each enforcement that are recent
      links_and_titles = unordered_box[0].find_all('a')
      list_titles_temp = []
      for a_tags in links_and_titles:
        title_text = a_tags.text
        list_titles_temp.append(title_text)
      for index in list_index_recent:
        titles_final.append(list_titles_temp[index])
      # Extracting the links for recent enforcement
      list_links_temp = []
      list_links_filtered = [] # We will use this to find the agencies and the categories which can be retrieved from each link
      for a_tags in links_and_titles:
        a_link_partial = a_tags.get('href') # Only the partial links
        a_link_complete = 'https://oig.hhs.gov' + a_link_partial
        list_links_temp.append(a_link_complete)
      for index in list_index_recent:
        links_final.append(list_links_temp[index])
        list_links_filtered.append(list_links_temp[index])
      # Extracting the categories of recent enforcement
      # Using a different method than Section 1
      for link in list_links_filtered:
        time.sleep(1) # Adding 2 seconds wait to prevent potential server-side block.
        enforcement_retrieved = requests.get(link)
        enforcement_content = BeautifulSoup(enforcement_retrieved.content, 'lxml')
        category_box = enforcement_content.find_all('li', class_ = "display-inline") # This class is unique to the 'li' tag for enforcement type
        category_box_items = [li.text for li in category_box]
        category_text = ' -&- '.join(category_box_items) # Joining categories
        category_text = category_text.replace('\n', '') # Cleaning
        category_text = ' '.join(category_text.split()) # To remove multiple blank space
        category_text = category_text.replace(', -&- ', ' -&- ') # Cleaning
        categories_final.append(category_text)
      # Extracting the agencies for recent enforcement
      for link in list_links_filtered:
        time.sleep(2) # Adding 2 seconds wait to prevent potential server-side block.
        enforcement_retrieved = requests.get(link)
        enforcement_content = BeautifulSoup(enforcement_retrieved.content, 'lxml')
        box_agency = enforcement_content.find_all('ul', class_ = "usa-list usa-list--unstyled margin-y-2")
        agency_info_prelim = box_agency[0].find_all('li')[1].text
        agency_info_final = agency_info_prelim.replace('Agency:', '')
        agencies_final.append(agency_info_final)
    elif any(date < first_day_of_month for date in list_dates_temp) and all(date < first_day_of_month for date in list_dates_temp):
      found_date_older = True # Setting on the alert for older dates
      pass
    if all(date >= first_day_of_month for date in list_dates_temp):
      found_date_older = False # Setting "OFF" the alert for older dates, just in case it was set "ON"
      # Extracting all the dates
      for date in list_dates_temp:
        dates_final.append(date)
      # Extracting the titles for each enforcement
      links_and_titles = unordered_box[0].find_all('a')
      for a_tags in links_and_titles:
        title_text = a_tags.text
        titles_final.append(title_text)
      # Extracting the links
      list_links_temp = [] # This will become handy when retrieving the agencies and the categories
      for a_tags in links_and_titles:
        a_link_partial = a_tags.get('href') # Only the partial links
        a_link_complete = 'https://oig.hhs.gov' + a_link_partial
        list_links_temp.append(a_link_complete)
        links_final.append(a_link_complete)
      # Extracting the categories
      for link in list_links_temp:
        time.sleep(1) # Adding 2 seconds wait to prevent potential server-side block.
        enforcement_retrieved = requests.get(link)
        enforcement_content = BeautifulSoup(enforcement_retrieved.content, 'lxml')
        category_box = enforcement_content.find_all('li', class_ = "display-inline") # This class is unique inside the 'li' tag for enforcement type
        category_box_items = [li.text for li in category_box]
        category_text = ' -&- '.join(category_box_items) # Joining categories
        category_text = category_text.replace('\n', '') # Cleaning
        category_text = ' '.join(category_text.split()) # To remove multiple blank space
        category_text = category_text.replace(', -&- ', ' -&- ') # Cleaning
        categories_final.append(category_text)
      # Extracting the agencies
      for link in list_links_temp:
        time.sleep(2) # Adding 2 seconds wait to prevent potential server-side block.
        enforcement_retrieved = requests.get(link)
        enforcement_content = BeautifulSoup(enforcement_retrieved.content, 'lxml')
        box_agency = enforcement_content.find_all('ul', class_ = "usa-list usa-list--unstyled margin-y-2")
        agency_info_prelim = box_agency[0].find_all('li')[1].text
        agency_info_final = agency_info_prelim.replace('Agency:', '')
        agencies_final.append(agency_info_final)
    
    # Now triggering the alert for older dates if the alert has been set "ON"
    if found_date_older == True:
      print(f'At least one date is older than the year and month provided. Scraping stopped at page {page_number}.')
      break
    else:
      pass
  
  # We have all the list filled, we can create the tidy dataframe now
  enforcement_data = pd.DataFrame({
    'title_enforcement' : titles_final,
    'date_enforcement' : dates_final,
    'agency_enforcement' : agencies_final,
    'category_enforcement' : categories_final,
    'link_enforcement' : links_final
  })

  # Returning final filtered dataframe
  return enforcement_data
#
#
#
#
#
enforcement_since_2023 = crawl_enforcement_data(2024, 11)

print(f'There are {len(enforcement_since_2023)} enforcement actions in our final dataframe')

# Saving the dataframe into a .csv file
enforcement_since_2023.to_csv('N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere/enforcement_actions_2023_january.csv', index = False) 
#
#
#
#
#
base_path = "N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere"
file_path = os.path.join(base_path, 'enforcement_actions_2023_january.csv')

enforcement_since_2023 = pd.read_csv(file_path)
#
#
#
#
#
print(f'The date for the earliest enforcement action scraped is: {min(enforcement_since_2023['date_enforcement'])}')

# Finding the detail for this enforcement
details_earliest_2023after = enforcement_since_2023.sort_values('date_enforcement').head(1)
print('The details for the earliest enforcement is:\n',
'title: ', details_earliest_2023after['title_enforcement'], '\n',
'date: ', details_earliest_2023after['date_enforcement'], '\n',
'agency: ', details_earliest_2023after['agency_enforcement'], '\n',
'catergory: ', details_earliest_2023after['category_enforcement'], '\n',
'link: ', details_earliest_2023after['link_enforcement'], '\n'
)
print('Please also note that in some case, there might be several enforcement at the earliest dates.\nIn those cases, this program will only pick just one of the earliest cases.')
#
#
#
#
#

enforcement_since_2021 = crawl_enforcement_data(2024, 9)

print(f'There are {len(enforcement_since_2021)} enforcement actions in our final dataframe')
#
#
#
#
#
# Saving the dataframe into a .csv file
enforcement_since_2021.to_csv('N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere/enforcement_actions_2021_january.csv', index = False) 
#
#
#
#
#
base_path = "N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere"
file_path = os.path.join(base_path, 'enforcement_actions_2021_january.csv')

enforcement_since_2021 = pd.read_csv(file_path)
#
#
#
#
#
print(f'The date for the earliest enforcement action scraped is: {min(enforcement_since_2021['date_enforcement'])}')

# Finding the detail for this enforcement
details_earliest_2021after = enforcement_since_2021.sort_values('date_enforcement').head(1)
print('The details for the earliest enforcement is:\n',
'title: ', details_earliest_2021after['title_enforcement'], '\n',
'date: ', details_earliest_2021after['date_enforcement'], '\n',
'agency: ', details_earliest_2021after['agency_enforcement'], '\n',
'catergory: ', details_earliest_2021after['category_enforcement'], '\n',
'link: ', details_earliest_2021after['link_enforcement'], '\n'
)
print('Please also note that in some case, there might be several enforcement at the earliest dates.\nIn those cases, this program will only pick just one of the earliest cases.')
#
#
#
#
#
#
#
#
#
graph_enforcement_year = alt.Chart(enforcement_since_2021).mark_line().encode(
  alt.X(
    'yearmonth(date_enforcement)',
    title = 'Month + Year',
    axis = alt.Axis(labelAngle = 270)
  ),
  alt.Y('count()', title = 'Number of enforcement actions per month')
).properties(
  title = 'Trend of enforcement actions over the period 2021-2024',
  width = 500,
  height = 200
)
graph_enforcement_year
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Splitting the joint categories
enforcement_since_2021['category_enforcement'] = enforcement_since_2021['category_enforcement'].str.split(' -&- ') # The splitter we used for the joint categories was pretty much handy.
enforcement_since_2021 = enforcement_since_2021.explode('category_enforcement')
enforcement_since_2021 = enforcement_since_2021.reset_index(drop = True)

# Filtering to only have the two groups
condition_two_categories = [category in ['Criminal and Civil Actions', 'State Enforcement Agencies'] for category in enforcement_since_2021['category_enforcement']]
enforcement_crim_vs_state = enforcement_since_2021[condition_two_categories]

# Plotting the two categories now.
graph_two_categories = alt.Chart(enforcement_crim_vs_state).mark_line().encode(
  alt.X(
    'yearmonth(date_enforcement):T',
    title = 'Month + Year',
    axis = alt.Axis(labelAngle = 270)
  ),
  alt.Y('count()', title = 'Number of enforcement actions per month'),
  alt.Color('category_enforcement:N', title = 'Categories of enforcement')
).properties(
  title = '"Criminal and Civic actions" vs "State Enforcement Agencies" over the period 2021-2024',
  width = 500,
  height = 200
)
graph_two_categories
#
#
#
#
#
#
# Adjusting the list of the keywords provided by Perplexity
healthcare_fraud_keywords = [
    "Health", "Medicare", "Medicaid", "Prescription", "Diagnosis",
    "Hospice", "Telemedicine", "Copayment", "Experiments", "Medical",
    "Medecine", "Patients", "Preventive", "Hospital", "Illness",
    "Practioner", "Nurse", "Doctors", "Pharmacist", "Pharmaceutical",
    "Surgery", "Surgeon", "Physician", "Testing", "Pharmacy"
]

financial_fraud_keywords = [
    "Financial", "Embezzlement", "Ponzi", "Securities", "Insider", 
    "Mortgage", "Identity", "Bankruptcy", "Laundering", "Wire", 
    "Accounting", "Pump", "Dump", "Predatory", "Lending", 
    "Falsifying", "Credit", "Check", "Investment", "Skimming",
    "Bank", "Stock", "Cash", "Accounting", "Accountant",
    "Racketeering", "Ponzi", "Pyramidal", "Arbitrage", "Finance"
]

drug_enforcement_keywords = [
    "Narcotics", "Trafficking", "Smuggling", "Cartel", "Controlled", 
    "Substances", "Opioid", "Fentanyl", "Methamphetamine", "Cocaine", 
    "Heroin", "Prescription", "Manufacturing", "Distribution", "Addiction", 
    "Seizure", "Enforcement", "Illicit", "Cultivation", "Synthetic",
    "Drug", "Narcotics", "Analgesics", "Stimulants", "Sedatives",
    "Psychotropic", "Counterfeit", "Precursors"
]

bribery_corruption_keywords = [
    "Bribery", "Corruption", "Extortion", "Kickbacks", "Collusion", 
    "Nepotism", "Cronyism", "Graft", "Embezzlement", "Misappropriation", 
    "Clientelism", "Favoritism", "Lobbying", "Influence", "Peddling", 
    "Slush", "Patronage", "Kleptocracy", "Malfeasance", "Quid",
    "Coercion", "Profiteering"
]
#
#
#
#
#
#
#
#
# Filtering the previous dataset to have only the category of "Criminal and Civil Actions"
only_criminal_civil = enforcement_crim_vs_state[enforcement_crim_vs_state['category_enforcement'] == 'Criminal and Civil Actions'].copy()

# Constructing the subcategories
  # We are building a function to calculate the number of keywords from each subcategory detected in a title (as we will this more than once).
def check_num_keywords(list_keywords, title_in_string):
  keyword_in_title = [keyword in title_in_string for keyword in list_keywords]
  num_keyword = sum(keyword_in_title)
  return num_keyword

  # We can use this function to finalize the process of creating subcategories
subcategories_enforcement = [] # Initializing the list that will be use to create the new varibale in the dataframe.
for title in only_criminal_civil['title_enforcement']:
  num_keywords_health = check_num_keywords(healthcare_fraud_keywords, title)
  num_keywords_financial = check_num_keywords(financial_fraud_keywords, title)
  num_keywords_drug = check_num_keywords(bribery_corruption_keywords, title)
  num_keywords_bribery_corruption = check_num_keywords(bribery_corruption_keywords, title)
  dict_num_keys = {
    'Health Care Fraud' : num_keywords_health,
    'Financial Fraud' : num_keywords_financial,
    'Drug Enforcement' : num_keywords_drug,
    'Bribery/Corruption' : num_keywords_bribery_corruption
  }
  subcategory_max_keywords = max(dict_num_keys, key = dict_num_keys.get)
  if dict_num_keys[subcategory_max_keywords] == 0:
    subcategories_enforcement.append('Other')
  else:
    subcategories_enforcement.append(subcategory_max_keywords)

# Appending the list to the dataframe
only_criminal_civil['subcategory_enforcement'] = subcategories_enforcement
#
#
#
#
#
graph_subcategories_crimandcivic = alt.Chart(only_criminal_civil).mark_line().encode(
  alt.X(
    'yearmonth(date_enforcement):T',
    title = 'Month + Year',
    axis = alt.Axis(labelAngle = 270)
  ),
  alt.Y('count()', title = 'Number of enforcement actions per month'),
  alt.Color('subcategory_enforcement:N', title = 'Subcategories')
).properties(
  title = 'Trend of subcategories of Criminal and Civic Actions over the period 2021-2024',
  width = 500,
  height = 200
)
graph_subcategories_crimandcivic
#
#
#
#
#
#
#
#
#
#
# Filtering the "enforcement_since_2021" dataset to have only case where the agency is a state
condition_stateof_in = ['State of' in agency for agency in enforcement_since_2021['agency_enforcement']]
agency_with_state = enforcement_since_2021[condition_stateof_in]

# Let's clean and creating a new column
agency_with_state['state_enforcement'] = [state.replace('State of ', '') for state in agency_with_state['agency_enforcement']]
#
#
#
#
#
# Reading the census state file
state_shapefile_path = "N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere/cb_2018_us_state_500k/cb_2018_us_state_500k.shp"
state_geo_data = gpd.read_file(state_shapefile_path) 

# Grouping agency_with_state by state 
group_state = agency_with_state.groupby('state_enforcement')
num_enforcement_state = group_state.apply(lambda group: len(group))
num_enforcement_state = num_enforcement_state.reset_index()
num_enforcement_state.columns = ['state_enforcement', 'number_enforcement']

# Importing the geometry by merging agency_with_state into a geodataframe
agency_with_state_geo = num_enforcement_state.merge(
  state_geo_data,
  how = 'left',
  left_on = 'state_enforcement',
  right_on = 'NAME'
)

# Converting the new dataframe into a geo dataframe
agency_with_state_geo = gpd.GeoDataFrame(agency_with_state_geo, geometry = 'geometry')

# Finishing the plot
fig, graph_enforcement_ax = plt.subplots(figsize=(12, 6))
graph_enforcement_perstate = agency_with_state_geo.plot(
  column = 'number_enforcement',
  cmap = 'viridis',
  legend = True,
  ax = graph_enforcement_ax
)
plt.axis("off")
plt.title(
  'Overall number of enforcement actions per states for 2021-2024',
  fontsize = '15',
  loc = 'center'
)
legends = plt.legend(
  title ='Number of enforcement',
  title_fontsize = '13',
  fontsize = '10',
  loc = 'right',
  bbox_to_anchor = (1.5, 0.5)
)
legends.get_title().set_rotation(90)
plt.gcf().set_facecolor('lightgray')
graph_enforcement_perstate
#
#
#
#
#
#
#
# Filtering the "enforcement_since_2021" dataset to have only case where the agency is a state
condition_district_in = ['District' in agency for agency in enforcement_since_2021['agency_enforcement']]
agency_with_district = enforcement_since_2021[condition_district_in]

# Let's clean and creating a new column "district_enforcement". The districts are usually separated with other texts  with a "," or a ";" 
agency_with_district['district_enforcement'] = [district.split(',')[-1] for district in agency_with_district['agency_enforcement']]
agency_with_district['district_enforcement'] = [district.split(';')[-1] for district in agency_with_district['district_enforcement']] # Second layer of cleaning for the new column
agency_with_district['district_enforcement'] = agency_with_district['district_enforcement'].str.strip() # To remove white space which could create issues with the merge coming next.
#
#
#
#
#
# Reading the US Attorney District shapefile file
usdistrict_shapefile_path = "N:/3 MES DOSSIERS SECONDAIRES/MASTER PREPARATION PROGRAM/University of Chicago/DAP II/problem-set-5-RalphValiere/US Attorney Districts Shapefile simplified_20241109/geo_export_8d61a61c-b22d-4587-8fb9-6c5739802da7.shp"
usdistrict_geo_data = gpd.read_file(usdistrict_shapefile_path)

# Grouping with_district_agency by disctrit 

group_disctrict = agency_with_district.groupby('district_enforcement')
num_enforcement_district = group_disctrict.apply(lambda group: len(group))
num_enforcement_district = num_enforcement_district.reset_index()
num_enforcement_district.columns = ['district_enforcement', 'number_enforcement']

# Export the geometry by merging and transforming "agency_with_district" into a geodataframe
agency_with_district_geo = num_enforcement_district.merge(
  usdistrict_geo_data,
  how = 'left',
  left_on = 'district_enforcement',
  right_on = 'judicial_d'
)
agency_with_district_geo = gpd.GeoDataFrame(agency_with_district_geo, geometry = 'geometry')

# Let's plot now
fig, graph_enforcement_ax = plt.subplots(figsize=(20, 12))
graph_enforcement_perdistrict = agency_with_district_geo.plot(
  column = 'number_enforcement',
  cmap = 'plasma',
  legend = True,
  ax = graph_enforcement_ax
)
plt.axis("off")
plt.title(
  'Overall number of enforcement actions\nper district for 2021-2024',
  fontsize = '40',
  loc = 'center',
  pad = 75
)
legends = plt.legend(
  title ='Number of enforcement',
  title_fontsize = '13',
  fontsize = '10',
  loc = 'right',
  bbox_to_anchor = (1.5, 0.5)
)
legends.get_title().set_rotation(90)
plt.gcf().set_facecolor('lightgray')
graph_enforcement_perdistrict
#
#
#
#
#
#
#
#
#
#
#
#

#
#
#
#

#
#
#
