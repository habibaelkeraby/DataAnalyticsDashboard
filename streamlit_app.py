import requests
import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import plost
from functions import *
import plotly.express as px

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
    columns=['Salutation',
     'Email',
     'Name',
     'City',
     'Attendance',
     'Company',
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
card1.metric(label="Countries", value=len(df_users['Country'].unique()))
card2.metric(label="Participants", value=len(df_users['Name'].unique()))
card3.metric(label="Companies", value=len(df_users['Company'].unique()))
card4.metric(label="Job Titles/Designations",
             value=len(df_users['Occupation'].unique()))
card5.metric(label="Industries Represented", value=len(df_users['Industry'].unique()))

####################

# REPORT SECTION 2
st.header("Profile Analysis")
# insert horizontal divider
st.divider()

col1, col2 = st.columns([0.3, 0.7], gap="large")

with col1:
    # Apply filter on the dataframe
    dynamic_filters = DynamicFilters(
        df_users, filters=['Country', 'Company', 'Occupation', 'Salutation'])
    st.write("Apply filters in any order 👇")
    dynamic_filters.display_filters(location='columns', num_columns=1)
    #dynamic_filters.display_df()
    df_filtered = dynamic_filters.filter_df()


with col2:

    # Create a pie chart to show the participant gender distribution
    #plost.pie_chart(data=df_filtered.groupby(
        #['user_salutation']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_salutation',
                    #title="Participants per Salutation")

    fig = px.pie(df_filtered.groupby(['Salutation'])['Name'].count().reset_index(),
         values='Name', names='Salutation', title='Participant per Salutation')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Salutation", on_select="rerun")

    # Create a bar chart to show the number of users per country
    #plost.bar_chart(data=df_filtered.groupby(
        #'country_name').user_name.count().reset_index(),
                    #bar='country_name',
                    #value='user_name',
                    #direction='horizontal',
                    #title="Participants per Country")

    fig = px.bar(df_filtered.groupby('Country')['Name'].count().reset_index(),
                 y='Name', x='Country', text='Name', title='Participants per Country')
    #fig.update_traces(texttemplate='%{text:s}', textposition='outside')
    #fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Country", on_select="rerun")


    # Create a pie chart to show the number of users per designation
    #plost.pie_chart(data=df_filtered.groupby(
        #['user_occupation']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_occupation',
                    #title="Participant Designation Distribution")

    fig = px.pie(df_filtered.groupby(['Occupation'])['Name'].count().reset_index(),
         values='Name', names='Occupation', title='Participant Designation Distribution')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Occupation", on_select="rerun",user_container_width=True)


    # Create a pie chart to show the participant attendance rate
    #plost.pie_chart(data=df_filtered.groupby(['user_attendance']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_attendance',
                    #title="Participant Attendance Rate")

    fig = px.pie(df_filtered.groupby(['Attendance'])['Name'].count().reset_index(),
         values='Name', names='Attendance', title='Participant Attendance Rate')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Attendance", on_select="rerun")
    
    # Create a pie chart to show the participant category distribution
    df_filtered['Category'] = df_filtered['Category'].apply(lambda x: ', '.join(x))
    df_categories = df_filtered['Category'].value_counts().reset_index()

    #plost.pie_chart(data=df_categories,
        #theta='count',
        #color='user_category',
        #title="Participant Category Distribution")
    
    fig = px.pie(df_categories, values='count', names='Category', title='Participant Category Distribution')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Category", on_select="rerun")

    # Create a pie chart to show the company size distribution
    df_filtered['Company Size'] = df_filtered['Company Size'].apply(lambda x: ', '.join(x))
   
    #plost.pie_chart(data=df_filtered.groupby(['company_size']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='company_size',
                    #title="Company Size Distribution")

    fig = px.pie(df_filtered.groupby(['Company Size'])['Name'].count().reset_index(),
                 values='Name', names='Company Size', title='Company Size Distribution')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Company Size", on_select="rerun")


    # Create a pie chart to show the partners wanted
    df_filtered['Partners'] = df_filtered['Partners'].apply(lambda x: ', '.join(x))

    #plost.pie_chart(data=df_filtered.groupby(['user_partners']).user_name.count().reset_index(),
                    #theta='user_name',
                    #color='user_partners',
                    #title="Partner Preference Distribution")

    fig = px.pie(df_filtered.groupby(['Partners'])['Name'].count().reset_index(),
         values='Name', names='Partners', title='Partner Preference Distribution')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, key="Partners", on_select="rerun")



####################

# REPORT SECTION 3
st.header("Cross Preference Analysis")
# insert horizontal divider
st.divider()


st.markdown("**Top Interests based on Participant Job Designation**")

# Create a df to store top interests per designation
interests_df = pd.DataFrame(columns=['Occupation/Designation', 'Top Interests'])

# Loop to find top interests for each unique designation
for i in range(len(df_users['Occupation'].unique())):
    # Append new row to df
    new_row = {
        "Occupation/Designation":
        df_users['Occupation'].unique()[i],
        "Top Interests":
        get_top_interests(df_users['Occupation'].unique()[i], df_users)
    }
    interests_df = pd.concat(
        [interests_df, pd.DataFrame([new_row])], ignore_index=True)

# Display df
st.dataframe(interests_df, use_container_width=True)

st.markdown("**What Companies are Offering & Seeking**")
df_company = df_users.groupby(['Company']).describe().reset_index()
df_company = df_company.iloc[:,[0,35,43,55]]
st.write(df_company, use_container_width=True)

# Insert horizontal divider
st.divider()
st.markdown('**All profile data**')
df_users = pd.DataFrame(
    all_data,
    columns=['Salutation',
             'Email',
             'Name',
             'City',
             'Attendance',
             'Company',
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
