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
  time.sleep(2) # Adding 2 seconds waitto prevent potential server-side block.
  page_numbers = hhsoig_enforce_content.find_all('a', class_ = "pagination__link")  
  last_page_contents = page_numbers[-1].text # Last page text always last index
  last_page = '' # Initializing the object that will store the last page string.
  for string in last_page_contents: #  Cleaning to find the correct text
    if string.isdigit():
      last_page = last_page + string
  last_page = int(last_page) # Converting the last page into an int type

  # Creating the foor loop to extract the data using the crawl
  for page_number in range(1,last_page + 1):
    page_link = hhsoig_enforcement_page + str(page_number)
    time.sleep(2) # Adding 2 seconds wait before going to the next page to prevent potential server-side block.
    page_path = requests.get(page_link)
    page_contents = BeautifulSoup(page_path.content, 'lxml')
    unordered_box = page_contents.find_all('ul', class_ = "usa-card-group padding-y-0") # Remember! All the info we need is contained in this unordered box list
    ####      
    # Extracting the data starting with the dates to filter.
    all_dates = unordered_box[0].find_all('span')
    list_dates_temp = [] # Temporary container for the dates
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


#
#
#
#
crawl_enforcement_data(2022, 12)
#
#
#
#

last_page + 1

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
a = 'aams'
ra
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
