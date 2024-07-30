# -*- coding: utf-8 -*-
"""Red Cross Donor Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pHeGLurAP7Kc0DI1UCiiOiY2SXxSXgvF
"""



"""Assigning the data URL"""

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzBYWDif8AqH47QpdaMsxZ0d3aXafgvL6EfnsUk6iN5QPCgrhvEky7hzI16iyfL3L2rfec3QX32JQj/pub?gid=0&single=true&output=csv'
url

url2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRgu-FVaZ2vZUJ4h0govtidayMH8BUrZFuRP1i99doumDNHvaYsbob5NtemG-Oly5AWXMT927JNIJaC/pub?gid=1502928385&single=true&output=csv'

"""importing pandas package for data processing"""

import pandas as pd
import numpy as np

"""Importng the data from the URL"""

data = pd.read_csv(url)

data

data2 = pd.read_csv(url2)

data2

"""Prepare the ZIP code columns for merging"""

data['DonorPostalCode'] = data['DonorPostalCode'].fillna(0).astype(int).astype(str)
data2['PHYSICAL ZIP'] = data2['PHYSICAL ZIP'].astype(str)

"""Merge the datasets on the ZIP code"""

merged_data = pd.merge(data, data2, left_on='DonorPostalCode', right_on='PHYSICAL ZIP', how='left')
merged_data

"""Data Cleaning and Preparation"""

# Checking for missing values
missing_values = data.isnull().sum()

# Checking data types
data_types = data.dtypes

missing_values, data_types

"""Displaying descriptive stats of the dataset"""

# Converting monetary columns to numeric
donation_columns = ['LastFiscalYearDonation', 'Donation2FiscalYearsAgo', 'Donation3FiscalYearsAgo', 'Donation4FiscalYearsAgo', 'Donation5FiscalYearsAgo', 'CurrentFiscalYearDonation', 'CumulativeDonationAmount']
for col in donation_columns:
    data[col] = data[col].replace('[\$,]', '', regex=True).astype(float)

# Descriptive statistics for numeric columns
desc_stats = data.describe()

desc_stats

"""Donor Demographics Analysis"""

import matplotlib.pyplot as plt

# Distribution of Donor Age
plt.figure(figsize=(10, 6))
data['DonorAge'].hist(bins=20, color='skyblue')
plt.title('Distribution of Donor Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Distribution of Gender Identity
plt.figure(figsize=(10, 6))
data['GenderIdentity'].value_counts().plot(kind='bar', color='lightgreen')
plt.title('Distribution of Gender Identity')
plt.xlabel('Gender')
plt.ylabel('Frequency')
plt.show()

"""Donation Patterns Analysis"""

# Total donations by fiscal year
total_donations_by_year = data[donation_columns].sum()

# Plotting total donations by fiscal year
plt.figure(figsize=(10, 6))
total_donations_by_year.plot(kind='bar', color='coral')
plt.title('Total Donations by Fiscal Year')
plt.xlabel('Fiscal Year')
plt.ylabel('Total Donations ($)')
plt.xticks(rotation=45)
plt.show()

# Average cumulative donation amount by gender
avg_cumulative_donation_by_gender = data.groupby('GenderIdentity')['CumulativeDonationAmount'].mean()

# Plotting average cumulative donation amount by gender
plt.figure(figsize=(10, 6))
avg_cumulative_donation_by_gender.plot(kind='bar', color='purple')
plt.title('Average Cumulative Donation Amount by Gender')
plt.xlabel('Gender')
plt.ylabel('Average Cumulative Donation Amount ($)')
plt.xticks(rotation=0)
plt.show()

"""Number of donors by state and city"""

donors_by_location = merged_data.groupby(['PHYSICAL STATE', 'PHYSICAL CITY']).size().reset_index(name='Number of Donors')
donors_by_location

merged_data['CurrentFiscalYearDonation'] = merged_data['CurrentFiscalYearDonation'].replace('[\$,]', '', regex=True).astype(float)

total_donations_by_location = merged_data.groupby(['PHYSICAL STATE', 'PHYSICAL CITY'])['CurrentFiscalYearDonation'].sum().reset_index(name='Total Donations')
total_donations_by_location

average_age_by_location = merged_data.groupby(['PHYSICAL STATE', 'PHYSICAL CITY'])['DonorAge'].mean().reset_index(name='Average Age')

# Display the result
print(average_age_by_location)

!pip install matplotlib seaborn
import matplotlib.pyplot as plt
import seaborn as sns

state_data = donors_by_location[donors_by_location['PHYSICAL STATE'] == 'CA']
plt.figure(figsize=(14, 8))
sns.barplot(data=state_data, x='PHYSICAL CITY', y='Number of Donors')
plt.xticks(rotation=90)
plt.title('Number of Donors by City in California')
plt.xlabel('City')
plt.ylabel('Number of Donors')
plt.show()

"""Identify the Top 10 Cities and States"""

top_cities = donors_by_location.nlargest(10, 'Number of Donors')
top_states = donors_by_location.groupby('PHYSICAL STATE')['Number of Donors'].sum().nlargest(10).reset_index()

print("Top 10 Cities:")
print(top_cities)

print("\nTop 10 States:")
print(top_states)

"""Visualizations for the Top 10 Cities and States"""

plt.figure(figsize=(14, 8))
sns.barplot(data=top_cities, x='PHYSICAL CITY', y='Number of Donors')
plt.xticks(rotation=90)
plt.title('Number of Donors by Top 10 Cities')
plt.xlabel('City')
plt.ylabel('Number of Donors')
plt.show()

plt.figure(figsize=(14, 8))
sns.barplot(data=top_states, x='PHYSICAL STATE', y='Number of Donors')
plt.xticks(rotation=90)
plt.title('Number of Donors by Top 10 States')
plt.xlabel('State')
plt.ylabel('Number of Donors')
plt.show()

"""Installing dataprep package to perform data profiling"""

!pip install dataprep

"""Importing data profiling report function form dataprep"""

from dataprep.eda import create_report

"""Creating data profiling report using dataprep"""

create_report(data).save()

"""Listing data features with more than 20% missing data"""

missing_data = data.isnull().sum()
missing_data

missing_data_columns = ['MaritalStatus','WealthRating','AcademicDegreeLevel', 'DonorDateOfBirth']

"""Fill missing values for simplicity"""

data['DonorAge'].fillna(data['DonorAge'].mean(), inplace=True)

"""Convert donation columns to numeric by removing dollar signs and converting to float"""

donation_cols = [
    'LastFiscalYearDonation', 'Donation2FiscalYearsAgo', 'Donation3FiscalYearsAgo',
    'Donation4FiscalYearsAgo', 'Donation5FiscalYearsAgo', 'CurrentFiscalYearDonation'
]

for col in donation_cols:
    data[col] = data[col].replace('[\$,]', '', regex=True).astype(float)

"""Convert binary columns to boolean"""

binary_cols = ['IsMemberFlag', 'IsAlumnusFlag', 'IsParentFlag', 'HasInvolvementFlag', 'HasEmailFlag', 'DonorIndicatorFlag.']
for col in binary_cols:
    data[col] = data[col].map({'Y': 1, 'N': 0})

"""Creating a dataset with features that have atleast 80% available data and dropping the features with more than 20% missing data."""

data80 = data.drop(missing_data_columns, axis = 1)
data80.columns

"""Defining noise variable based on the qualitative data prep efforts"""

ignored_cols = ['DonorUniqueId', 'PreferredAddressType', 'IsMemberFlag', 'CumulativeDonationAmount', 'DonorPostalCode','MaritalStatus','WealthRating','AcademicDegreeLevel', 'DonorDateOfBirth']

"""Defining the predictors dataset"""

predictors = data.drop(ignored_cols, axis = 1)
predictors.columns

"""Installing sweetviz package to perform statistcal EDA"""

!pip install sweetviz

"""Importing Sweetviz package to perform statistical EDA"""

import sweetviz as sv

"""Generating EDA data profiling report using sweetviz"""

sv_report = sv.analyze(predictors)

"""Generating an HTML report using sweetviz profiling report"""

sv_report.show_html('Red Cross Donor Prediction Report.html')

"""Correlations"""

correlation_matrix = predictors.corr()
correlation_matrix

"""Setting the dependent variable/ target"""

y = 'DonorIndicatorFlag.'

"""Defining Numerical variables"""

num_cols = ['DonorAge', 'ConsecutiveDonorYears', 'LastFiscalYearDonation', 'Donation2FiscalYearsAgo',
                  'Donation3FiscalYearsAgo', 'Donation4FiscalYearsAgo', 'Donation5FiscalYearsAgo',
                  'CurrentFiscalYearDonation']

"""Defining Categorical variables"""

cat_cols = ['GenderIdentity', 'IsAlumnusFlag', 'IsParentFlag', 'HasInvolvementFlag']

"""Installing pycaret - Auto AIML package"""

!pip install -U --pre pycaret

"""Importing all categorical libariries from pycaret"""

import numpy as np

from pycaret.classification import *

"""Setting up pycaret with the data for ML modeling"""

import numpy as np

# Check for extremely small values in the numeric columns
for col in num_cols:
    print(f"Minimum value in {col}: {predictors[col].min()}")

# Define a threshold
threshold = 1e-10

# Replace values smaller than the threshold
predictors[num_cols] = predictors[num_cols].applymap(lambda x: x if abs(x) > threshold else threshold)

# Ignore underflow errors
np.seterr(under='ignore')

from pycaret.classification import setup

# Set up PyCaret
classification_setup = setup(data=predictors, target=y, categorical_features=cat_cols, numeric_features=num_cols, session_id=123)

"""Invoking ML algorithms"""

compare_models()

"""Building a classification ML model using gbc"""

gbc_model = create_model('gbc')

"""model correlations"""

model_correlations = evaluate_model(gbc_model)