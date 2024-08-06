import requests
import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import plost
from functions import *
import plotly.express as px


#_____________________
import requests
# /?event_id=57
#https://dataanalyticsdashboard-j5rfvadj3jkj7cda5vutul.streamlit.app/?eventId=65facda87c22b11303c0a4b8&token=Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI5S3N3UlVVeE8zcDFHcjZUOVQ4d0MzUWpZUFVfVGNoajU0Z21fczBFM2NBIn0.eyJleHAiOjE3MjI5NDY4MDYsImlhdCI6MTcyMjk0NjUwNiwiYXV0aF90aW1lIjoxNzIyOTQ0Mzk3LCJqdGkiOiJlZDViMzI0OS0xMGYyLTQxNTUtYTU1MC1kNTU4YjIwNDNkM2EiLCJpc3MiOiJodHRwczovL2xvZ2luLXN0YWdlLndlbGNvbWUuYXBwc2F5YS5jb20vcmVhbG1zL3dlbGNvbWUtcmVhbG0iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiY2E0MGJjMmEtNDZmMi00OTZmLTk1MWYtYzg4MGY4YjZiYmY0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViYXBwIiwibm9uY2UiOiJaMVpEUldSM1NTNUdUbTVtWTJwWmRUbDJSelphUWxjNVdteFpNME5mYzNKdVdVVm9hSEJLWkZoVmFVOUoiLCJzZXNzaW9uX3N0YXRlIjoiZWYxMGM4MjAtZjE3ZS00MGNjLWIzZjQtZWFiYzhhNjZmYTIyIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL3N0YWdlLXdlbGNvbWUuYXBwc2F5YS5jb20iLCIqIiwiaHR0cHM6Ly9tYW5hZ2VyLXN0YWdlLndlbGNvbWUuYXBwc2F5YS5jb20iLCJodHRwOi8vbG9jYWxob3N0OjQyMDAiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMtd2VsY29tZS1yZWFsbSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIG9mZmxpbmVfYWNjZXNzIiwic2lkIjoiZWYxMGM4MjAtZjE3ZS00MGNjLWIzZjQtZWFiYzhhNjZmYTIyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVzZXJfaWQiOiJjYTQwYmMyYS00NmYyLTQ5NmYtOTUxZi1jODgwZjhiNmJiZjQiLCJuYW1lIjoiQW5hcyBTYWJiYW5pIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYW5hcy5zYWJiYW5pQGdtYWlsLmNvbSIsImdpdmVuX25hbWUiOiJBbmFzIiwiZmFtaWx5X25hbWUiOiJTYWJiYW5pIiwiZW1haWwiOiJhbmFzLnNhYmJhbmlAZ21haWwuY29tIn0.jNr7nQGil8Xe0DlI6KHuzdwmBrjmc6wVWG1ySgi5_NvNFpFPlm_aA4_JZLJgY2w0Kq3a6PhvmoQiuseoLdxaDsCALaA47xrjr1C6jpDEhawR8Pd0I1TbD7vZScLFp1WR9RP316fnoBnAKjOPpSq7miLaNa1_HhwPzRMo13nD8-3ju5bNx3Pv3uZt7Cwm5GDOFHd_jGhsaFdik8qcFZL_FoOWrvXf1eycEc35-vhrXn2Zm_sAKN6ST1PtvtC7-yC55HI_i_KbQaToKQ7ZoVIKVVfmTBiBktMmUPrlfyK106JqoHHPCOH_fMnLUOiF2imVn7uzOgG4Trrb57YOlf3CXw
eventId = st.query_params["eventId"]
token = st.query_params["token"]
#event_id = str(57)
size=100
r = requests.get('https://manager-stage.welcome.appsaya.com/api/profile/search?eventId='+eventId+'&page=0&size=100&sort=createdAt,desc',headers={'Authorization':token})
#data = r.json()

st.write(token)
st.write(r.json())
st.write(r.request.headers)


#_________________


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
