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
from shapely import Polygon, Point
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
#
hhsoig_enforce_path = r'https://oig.hhs.gov/fraud/enforcement/'

hhsoig_enforce_retrived = requests.get(hhsoig_enforce_path)

hhsoig_enforce_content = BeautifulSoup(hhsoig_enforce_retrived.content, 'lxml') # We can use 'html.parser' if 'lxml' is not working
#
#
#
#
#
# Retrieving the unordered list ('ul') we will need to find the list of enforcement in the first page on the website. This will present us from retrieving all the elements ('li') from this website. Only retrieving the one we want.
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
  a_link_partial = a_tags.get('href') # We have noticed that the links are partial links
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
# Extracting the 'span' tags from our 'ul' list
list_dates_ongoing = list_enforce_firstpage[0].find_all('span')
list_dates_final = [] # Initializing the list of dates we will append
for span_tags in list_dates_ongoing:
  date_text = span_tags.text
  list_dates_final.append(date_text)

# Now let's change the format of the dates text to later transform it into a date data type
# We will replace all the space by "/" and remove all the "," to have a uniform format.

for index in range(len(list_dates_final)):
  list_dates_final[index] = list_dates_final[index].replace(' ', '/')
  list_dates_final[index] = list_dates_final[index].replace(',', '')

# Now let's convert the month name into month rank number
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
list_category_final = [] # Initializing the list of category we will append
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

# Building the for loop to go over each link in "enforcement_action_data" and retrieve the agency name, and store it in "list_agency_final".
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
#
# Base path for the enforcement action webpages
hhsoig_enforcement_page = r'https://oig.hhs.gov/fraud/enforcement/?page='

# This function is going to be long. So sorry for the graders!

def crawl_enforcement_data(year, month):
  # Verifying validity for month
  if type(month) != int:
    print('TypeError: Argument "month" only accepts int type.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit"')
    sys.exit() # This will exit the code and not run any other lines.
  elif month < 1 or month > 12:
    print('RangeError: Argument "month" only accepts values from 0 to 12.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit"')
    sys.exit() # This will exit the code and not run any other lines.
  else:
    pass

  # Verifying validity for year
  if type(year) != int:
    print('TypeError: Argument "year" only accepts int type.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit"')
    sys.exit() # This will exit the code and not run any other lines.
  elif len(str(year)) != 4:
    print('FormatError: Please enter the "year" in the correct format (e.g. 1804)\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit"')
    sys.exit() # This will exit the code and not run any other lines.
  elif year < 2013 or  year > int(datetime.datetime.now().year):
    print(f'RangeError: Argument "year" only accepts values from 2013 to {int(datetime.datetime.now().year)}.\nThis is Ralph predefined error message. Another message will also be displayed after exiting the system. Please ignore message "SystemExit"')
    sys.exit()
  else:
    pass

  # Iniatizaling the lists that will serve to append the tidy dataframe
  titles_final = []
  dates_final = []
  categories_final= []
  links_final = []
  agencies_final = []
  list_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] # This will be handy for conversion
  rank_month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'] # For future conversion

  # Finding the number of pages we will iterate for our crawling
  time.sleep(1) # Adding 2 seconds waitto prevent potential server-side block.
  page_numbers = hhsoig_enforce_content.find_all('a', class_ = "pagination__link")  
  last_page_contents = page_numbers[-1].text # Last page text always last index
  last_page = '' # Initializing the object that will store the last page string.
  for string in last_page_contents: #  Cleaning to find the correct text
    if string.isdigit():
      last_page = last_page + string
  last_page = int(last_page) # Converting the last page into an int type

  # Creating the foor loop to extract the data using the crawl
  for page_number in range(1, 7):
    page_link = hhsoig_enforcement_page + str(page_number)
    time.sleep(1) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
    page_path = requests.get(page_link)
    page_contents = BeautifulSoup(page_path.content, 'lxml')
    unordered_box = page_contents.find_all('ul', class_ = "usa-card-group padding-y-0") # Remember! All the info we need is contained in this unordered box list
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
    for index in range(len(list_dates_temp)): # To convert month name into month rank
      month_name = list_dates_temp[index].split('/')[0] # To find month name of the date
      index_month = list_months.index(month_name) # The list of months came handy
      list_dates_temp[index] = list_dates_temp[index].replace(month_name, rank_month[index_month])
    for index in range(len(list_dates_temp)): # Converting into date type
      list_dates_temp[index] = datetime.datetime.strptime(list_dates_temp[index], '%m/%d/%Y')
      ## Generating a date object as reference to better filter
    first_day_of_month = str(month) + '/1/' + str(year) 
    first_day_of_month = datetime.datetime.strptime(first_day_of_month, '%m/%d/%Y')
      ## Checking for older date and retrieving dates
    if any(date < first_day_of_month for date in list_dates_temp) and (not all(date < first_day_of_month for date in list_dates_temp)):
      found_date_older = True # Setting on the alert for older dates
      list_index_recent = [] # To store the index for dates NOT older
      for index in range(len(list_dates_temp)):
        if list_dates_temp[index] >= first_day_of_month:
          list_index_recent.append(index)
        else:
          pass
      # Now we can append to the final list of dates
      for index in list_index_recent:
        dates_final.append(list_dates_temp[index])
      # Can also find the other variables, which will depend on the list of index for recent dates. The values for each index will match
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
      list_links_filtered = [] # We will use this to find the agencies and the categories which are retrieved from inside each link
      for a_tags in links_and_titles:
        a_link_partial = a_tags.get('href') # Only the partial links
        a_link_complete = 'https://oig.hhs.gov' + a_link_partial
        list_links_temp.append(a_link_complete)
      for index in list_index_recent:
        links_final.append(list_links_temp[index])
        list_links_filtered.append(list_links_temp[index])
      # Extracting the categories of recent enforcement
      # Using a different method than in Section 1
      for link in list_links_filtered:
        time.sleep(1) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
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
        time.sleep(2) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
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
      found_date_older = False # Setting off the alert for older dates
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
        time.sleep(1) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
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
        time.sleep(2) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
        enforcement_retrieved = requests.get(link)
        enforcement_content = BeautifulSoup(enforcement_retrieved.content, 'lxml')
        box_agency = enforcement_content.find_all('ul', class_ = "usa-list usa-list--unstyled margin-y-2")
        agency_info_prelim = box_agency[0].find_all('li')[1].text
        agency_info_final = agency_info_prelim.replace('Agency:', '')
        agencies_final.append(agency_info_final)
    
    # Now triggering the aler for older dates if the alert has been set on
    if found_date_older == True:
      print(f'At least one date is older than the year and month provided. Scraping stopped at page {page_number}.')
      break
    else:
      pass
  
  # We have all the list filled, we can create the tidy dataframe now
  enforcement_data_after2013 = pd.DataFrame({
    'title_enforcement' : titles_final,
    'date_enforcement' : dates_final,
    'agency_enforcement' : agencies_final,
    'category_enforcement' : categories_final,
    'link_enforcement' : links_final
  })

  # Returning final filtered dataframe
  return enforcement_data_after2013
#
#
#
#
temp_test_november2024 = crawl_enforcement_data(2024, 11)
temp_test_november2024
#
#
#

temp_test_october2024
#
#
#
#
#
############################################################################
##### Remember to change this code to adapt it to the 2023 real dataset ####
############################################################################

temp_test_november2024 = crawl_enforcement_data(2024, 11)

print(f'There are {len(temp_test_november2024)} in our final dataframe')
#
#
#
#
#
############################################################################
##### Remember to change this code to adapt it to the 2023 real dataset ####
############################################################################

print(f'The date for the earliest enforcement action scraped is: {min(temp_test_november2024['date_enforcement'])}')

# Finding the detail for this enforcement
details_earliest_2023after = temp_test_november2024.sort_values('date_enforcement').head(1)
print('The details for the earliest enforcement is:\n',
'title: ', details_earliest_2023after['title_enforcement'], '\n',
'date: ', details_earliest_2023after['date_enforcement'], '\n',
'agency: ', details_earliest_2023after['agency_enforcement'], '\n',
'catergory: ', details_earliest_2023after['category_enforcement'], '\n',
'link: ', details_earliest_2023after['link_enforcement'], '\n'
)
#
#
#
#
#
temp_test_october2024 = crawl_enforcement_data(2024, 10)

print(f'There are {len(enforcement_data_2021andafter)} in our final dataframe')
#
#
#
print(f'There are {len(enforcement_data_2021andafter)} in our final dataframe')
#
#
#
#
#
print(f'The date for the earliest enforcement action scraped is: {min(enforcement_data_2021andafter['date_enforcement'])}')

# Finding the detail for this enforcement
details_earliest_2021after = enforcement_data_2021andafter.sort_values('date_enforcement').head(1)
print('The details for the earliest enforcement is:\n',
'title: ', details_earliest_2021after['title_enforcement'], '\n',
'date: ', details_earliest_2021after['date_enforcement'], '\n',
'agency: ', details_earliest_2021after['agency_enforcement'], '\n',
'catergory: ', details_earliest_2021after['category_enforcement'], '\n',
'link: ', details_earliest_2021after['link_enforcement'], '\n'
)
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
#
#

#
#
#
