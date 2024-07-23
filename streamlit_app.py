import requests
import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import plost
from functions import *

st.set_page_config(
    page_title="Data Analysis Report DEMO",
    page_icon="📊",
    layout="wide",
    #initial_sidebar_state="expanded"
)

# Fetching data
dataset = pd.read_json('profile.json')
#st.write(dataset)
#st.write(dataset.iloc[0])

# initialize list of lists
all_data = []
size = len(dataset)

for i in range(size):
    data = dataset.iloc[i]

    user_salutation = data['salutation']
    user_email = data['email']
    user_name = data['firstName'] + " " + data['lastName']
    user_city = data['businessCity']
    user_attendance = data['presentAtEventVenue']
    company_name = data['company']
    country_name = data['country']['name']
    user_occupation = data['occupation']
    user_industry = data['myIndustry']['name']
    user_offers = data['myOffers']
    if len(user_offers) == 0:
      user_offerlist == []
    else:
      user_offerlist = [offer['name']for offer in user_offers]
    
    user_interests = data['myInterests']
    user_interestlist = [industry['name'] for industry in user_interests]
    user_lookingfor = data['lookingFor']
    user_lookingforlist = [element['label'] for element in user_lookingfor]
    user_category = data['metaField']['je suis :']
    company_size = data['metaField']['quelle est la taille de votre entreprise ?']
    user_partners = data['metaField']['quel type de partenaire recherchez-vous ?']
    profile = [user_salutation,
      user_email,
      user_name,
      user_city,
      user_attendance,
      company_name,
      country_name,
      user_occupation,
      user_industry,
      user_offerlist,
      user_interestlist,
      user_lookingforlist,
      user_category,
      company_size,
      user_partners]
    all_data.append(profile)


# Create the pandas DataFrame for users
df_users = pd.DataFrame(
    all_data,
    columns=['user_salutation',
          'user_email',
          'user_name',
          'user_city',
          'user_attendance',
          'company_name',
          'country_name',
          'user_occupation',
          'user_industry',
          'user_offerlist',
          'user_interestlist',
          'user_lookingforlist',
          'user_category',
          'company_size',
          'user_partners']
)

df_users.fillna("Not Specified", inplace=True)
#st.write(df_users)


####################
# DATA VISUALIZATION SECTION

# dashboard title
st.title("Data Analysis Dashboard - DEMO")

# REPORT SECTION 1


st.header("**An Overview in Numbers**")

# insert horizontal divider
st.divider()

# create 4 columns for number cards
card1, card2, card3, card4, card5 = st.columns(5)
# fill in those three columns with respective metrics or KPIs
card1.metric(label="Countries", value=len(df_users.country_name.unique()))
card2.metric(label="Participants", value=len(df_users.user_name.unique()))
card3.metric(label="Companies", value=len(df_users.company_name.unique()))
card4.metric(label="Job Titles/Designations",
             value=len(df_users.user_occupation.unique()))
card5.metric(label="Industries Represented", value=len(df_users.user_industry.unique()))

####################

# REPORT SECTION 2
st.header("Profile Analysis")
# insert horizontal divider
st.divider()

col1, col2 = st.columns([0.3, 0.7], gap="large")

with col1:
    # Apply filter on the dataframe
    dynamic_filters = DynamicFilters(
        df_users, filters=['country_name', 'company_name', 'user_occupation'])
    st.write("Apply filters in any order 👇")
    dynamic_filters.display_filters(location='columns', num_columns=1)
    #dynamic_filters.display_df()
    df_filtered = dynamic_filters.filter_df()


with col2:

    # Create a pie chart to show the participant gender distribution
    plost.pie_chart(data=df_filtered.groupby(
        ['user_salutation']).user_name.count().reset_index(),
                    theta='user_name',
                    color='user_salutation',
                    title="Participants per Salutation")

    # Create a bar chart to show the number of users per country
    plost.bar_chart(data=df_filtered.groupby(
        'country_name').user_name.count().reset_index(),
                    bar='country_name',
                    value='user_name',
                    direction='horizontal',
                    title="Participants per Country")


    # Create a pie chart to show the number of users per designation
    plost.pie_chart(data=df_filtered.groupby(
        ['user_occupation']).user_name.count().reset_index(),
                    theta='user_name',
                    color='user_occupation',
                    title="Participant Designation Distribution")


    # Create a pie chart to show the participant attendance rate
    plost.pie_chart(data=df_filtered.groupby(['user_attendance']).user_name.count().reset_index(),
                    theta='user_name',
                    color='user_attendance',
                    title="Participant Attendance Rate")
    
    # Create a pie chart to show the participant category distribution
    df_filtered['user_category'] = df_filtered['user_category'].apply(lambda x: ', '.join(x))
    df_categories = df_filtered['user_category'].value_counts().reset_index()

    plost.pie_chart(data=df_categories,
        theta='count',
        color='user_category',
        title="Participant Category Distribution"
       )

    # Create a pie chart to show the company size distribution
    df_filtered['company_size'] = df_filtered['company_size'].apply(lambda x: ', '.join(x))
   
    plost.pie_chart(data=df_filtered.groupby(['company_size']).user_name.count().reset_index(),
                    theta='user_name',
                    color='company_size',
                    title="Company Size Distribution")




    # Create a pie chart to show the partners wanted
    df_filtered['user_partners'] = df_filtered['user_partners'].apply(lambda x: ', '.join(x))

    plost.pie_chart(data=df_filtered.groupby(['user_partners']).user_name.count().reset_index(),
                    theta='user_name',
                    color='user_partners',
                    title="Partner Preference Distribution")
    


####################

# REPORT SECTION 3
st.header("Cross Preference Analysis")
# insert horizontal divider
st.divider()


st.markdown("**Top Interests based on Participant Job Designation**")

# Create a df to store top interests per designation
interests_df = pd.DataFrame(columns=['user_occupation', 'top_interests'])

# Loop to find top interests for each unique designation
for i in range(len(df_users.user_occupation.unique())):
    # Append new row to df
    new_row = {
        "user_occupation":
        df_users.user_occupation.unique()[i],
        "top_interests":
        get_top_interests(df_users.user_occupation.unique()[i], df_users)
    }
    interests_df = pd.concat(
        [interests_df, pd.DataFrame([new_row])], ignore_index=True)

# Display df
st.dataframe(interests_df)

# Insert horizontal divider
st.divider()
st.markdown('**All profile data**')
df_users = pd.DataFrame(
    all_data,
    columns=['Salutation',
             'Email',
             'Full Name',
             'City',
             'Attendance',
             'Company Name',
             'Country',
             'Occupation',
             'Industry',
             'Offers',
             'Interests',
             'Looking for',
             'Category',
             'Company Size',
             'Partners']
)
st.write(df_users)
