import requests
import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import plost
from functions import *

st.set_page_config(
  page_title="Post-Event Data Analysis Report",
  page_icon="📊",
  layout="wide",
  #initial_sidebar_state="expanded"
)


# Fetching data from API

@st.cache_data
def fetch_data():
  event_link = "https://newstage.biz-match.appsaya.com/"
  eventId = 10
  API_KEY = "W3kwgy2Tn40zr0rHwBFL18ov4Bb5FHA5eZw9CC38knZBb"
  size = 37
  pageNumber = 0
  url = event_link + "api/users/search/findByEventIdAndGroupId?projection=withUserGroup&eventId=" + str(eventId) + "&groupId=2&size=" + str(size) + "&page=" + str(pageNumber)
  r = requests.get(url, headers={"X-BIZMATCH-API-KEY":API_KEY})
  
  # initialize list of lists
  all_data = []
  
  dataset = r.json()
  users = dataset['_embedded']['users']
  max_page = dataset['page']['totalPages']
    
  while pageNumber < max_page:
    for i in range(size):
      data = users[i]
      user_data = extract_user_data(data)
      all_data.append(user_data)
    pageNumber += 1
    r = requests.get(url, headers={"X-BIZMATCH-API-KEY":API_KEY})
    dataset = r.json()
    users = dataset['_embedded']['users']

  return all_data

all_data = fetch_data()

# Create the pandas DataFrame
df = pd.DataFrame(all_data, 
                  columns=['user_salutation',
                           'user_name',
                           #'user_level',
                           'user_designation',
                           'user_email',
                           'user_verified',
                           'country_name',
                           'country_region',
                           'country_subregion',
                           'company_name',
                           'company_industrylist',
                           'user_wanteddeals',
                           'user_interestlist'
                      ]
                  )

df.fillna("Not Specified",inplace=True)
#st.write(df)

####################
# DATA VISUALIZATION SECTION

# dashboard title
st.title("Post-Event Data Analysis Dashboard")


# REPORT SECTION 1
st.header("Attendee Demographics")
# insert horizontal divider
st.divider()

st.markdown("**An Overview in Numbers**")
# create 4 columns for number cards
card1, card2, card3, card4 = st.columns(4)
# fill in those three columns with respective metrics or KPIs
card1.metric(
    label="Countries",
    value=len(df.country_name.unique())
)
card2.metric(
    label="Participants",
    value=len(df.user_name.unique())
)
card3.metric(
    label="Companies",
    value=len(df.company_name.unique())
)
card4.metric(
    label="Job Titles/Designations",
    value=len(df.user_designation.unique())
)
# insert horizontal divider
st.divider()

col1, col2 = st.columns([0.3, 0.7], gap="large")
#df_filtered=df[['user_name','country_name','country_region', 'country_subregion','company_name', 'user_designation']]
with col1:
  # Apply filter on the dataframe
  dynamic_filters = DynamicFilters(df, filters=['country_name', 'company_name', 'user_designation'])
  st.write("Apply filters in any order 👇")
  dynamic_filters.display_filters(location='columns', num_columns=1)
  #dynamic_filters.display_df()
  df_filtered = dynamic_filters.filter_df()

  # top-level filters
  #df_filtered = df
  #designation_filter = st.selectbox("Select the Job Designation",pd.unique(df["user_designation"]),index=None)
  # creating a single-element container
  #placeholder = st.empty()
  # dataframe filter
  #df_filtered = df[df["user_designation"] == designation_filter]

with col2:

  # Create a pie chart to show the participant gender distribution
  plost.pie_chart(
    data=df_filtered.groupby(['user_salutation']).user_name.count().reset_index(),
    theta='user_name',
    color='user_salutation',
    title="Participants per Salutation"
    )


  # Create a bar chart to show the number of users per country
  plost.bar_chart(
      data=df_filtered.groupby('country_name').user_name.count().reset_index(),
      bar='country_name',
      value='user_name',
      direction='horizontal',
      title="Participants per Country"
  )

  # Create a bar chart to show the number of users per region
  plost.bar_chart(
    data=df_filtered.groupby(['country_region']).user_name.count().reset_index(),
      bar='country_region',
      value='user_name',
      color='country_region',
      direction='horizontal',
      title="Participant Geographic Distribution"
  )

  # Detailed view of geographical data
  with st.expander("View details of participant distribution by geographical region:"):
    st.write(df_filtered.groupby(['country_region', 'country_subregion']).user_name.count().reset_index())
    
  # Create a pie chart to show the number of users per designation
  plost.pie_chart(
      data=df_filtered.groupby(['user_designation']).user_name.count().reset_index(),
      theta='user_name',
      color='user_designation',
      title="Participant Designation Distribution"
      )


####################

# REPORT SECTION 2
st.header("Engagement Analysis")
# insert horizontal divider
st.divider()

# Create a pie chart to show the participant gender distribution
plost.pie_chart(
  data=df.groupby(['user_verified']).user_name.count().reset_index(),
  theta='user_name',
  color='user_verified',
  title="Participant Account Verification Rate"
  )

####################

# REPORT SECTION 3
st.header("Cross Preference Analysis")
# insert horizontal divider
st.divider()

st.markdown("**Top Interests based on Participant Job Designation**")

# Create a df to store top interests per designation
designation_df = pd.DataFrame(columns=['user_designation','top_interests'])

# Loop to find top interests for each unique designation
for i in range(len(df.user_designation.unique())):
  # Append new row to df
  new_row = {"user_designation": df.user_designation.unique()[i], "top_interests": get_top_interests(df.user_designation.unique()[i], df)}
  designation_df = pd.concat([designation_df, pd.DataFrame([new_row])], ignore_index=True)

# Display df
st.dataframe(designation_df)