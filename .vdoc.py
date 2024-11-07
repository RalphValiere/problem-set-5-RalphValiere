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
from bs4 import BeautifulSoup
import requests
import warnings
import numpy as np
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
#
#
#
#
#

#
#
#
#
#
#

#
#
#
#
#
#

#
#
#
#

#
#
#
#

#
#
#
