# FUNCTIONS FILE


#####################

'''
Function to filter df by designation given as input (filter_item)
Output is list of top 5 interests related to the designation given
'''

def get_top_interests(filter_term, df):
  # Filter df by designation specified
  filtered_df = df[df["user_occupation"]==filter_term]
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

'''
Function to filter df by designation given as input (filter_item)
Output is list of top 5 industries related to the designation given
'''

def get_top_industries(filter_term, df):
  # Filter df by designation specified
  filtered_df = df[df["user_occupation"]==filter_term]
  # Extract all interests selected
  industry_list = filtered_df["company_industrylist"].explode().unique() 
  # Remove nested lists
  industry_list = [str(item) for item in industry_list if not isinstance(item,list)]
  # Join all items as a single string then split 
  industry_list = ','.join(industry_list).split(",")
  # Count the instances of each unique item
  from collections import Counter
  mydict = Counter(industry_list)
  # Return top five results
  return sorted(mydict, key=mydict.get, reverse=True)[0:4]

#####################