# FUNCTIONS FILE

#####################
'''
Function to read relevant information of user
Output is list of relevant user data to be appended to dataframe
'''


def extract_user_data(data):

  # Relevant data

  # User details
  user_salutation = data['salutation']
  user_name = data['name']
  #user_level = data['level']['level']
  user_designation = data['designation']
  user_email = data['emailAddress']
  user_verified = data['emailVerified']

  # Geographical data
  if data['company']['country'] == None:
    country_name = None
    country_region = None
    country_subregion = None
  else:
    country_name = data['company']['country']['name']
    country_region = data['company']['country']['region']
    country_subregion = data['company']['country']['subregion']

  # Company details
  company_name = data['company']['name']
  company_industries = data['company']['category']
  company_industrylist = [industry['name'] for industry in company_industries]

  # Wanted deals & Interests
  user_wanteddeals = data['company']['wantedDeal']
  user_interests = data['interestedIndustry']
  user_interestlist = [industry['name'] for industry in user_interests]

  # Gather into list
  user_data = [user_salutation,
             user_name,
             #user_level,
             user_designation,
             user_email,
             user_verified,
             country_name,
             country_region,
             country_subregion,
             company_name,
             company_industrylist,
             user_wanteddeals,
             user_interestlist]

  return user_data
#####################

'''
Function to filter df by designation given as input (filter_item)
Output is list of top 5 interests related to the designation given
'''

def get_top_interests(filter_term, df):
  # Filter df by designation specified
  filtered_df = df[df["user_designation"]==filter_term]
  # Extract all interests selected
  interest_list = filtered_df["user_interestlist"].explode().unique() 
  # Remove nested lists
  interest_list = [str(item) for item in interest_list if not isinstance(item,list)]
  # Join all items as a single string then split 
  interest_list = ','.join(interest_list).split(",")
  # Count the instances of each unique item
  from collections import Counter
  mydict = Counter(interest_list)
  # Return top five results
  return sorted(mydict, key=mydict.get, reverse=True)[0:4]

#####################