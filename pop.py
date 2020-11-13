import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

alt.data_transformers.disable_max_rows()

ind = pd.read_csv('individual.csv').iloc[:,1:]
ind = ind.replace('Unknown','Unknown or Missing')
ind = ind.replace('Missing','Unknown or Missing')

session = st.sidebar.selectbox("Parameter", ["Death Rate", ""])
st.title('COVID-19 (Population Data)')

st.write("""

	The  death count of different races 








	""")

histogram = alt.Chart(ind[(ind['death_yn'] != 'Unknown or Missing') & (ind['sex'] !='Unknown or Missing') ]).mark_bar().encode(
    x='race_ethnicity_combined',
    y='count(death_yn):Q',
    color = 'race_ethnicity_combined',
    column = 'sex')

st.altair_chart(histogram)


ages = ind[['sex','age_group','medcond_yn']]
ages['No'] = np.zeros(len(ages))
ages['Yes'] = np.zeros(len(ages))
ages['Unknown or Missing'] = np.zeros(len(ages))
for i in range(len(ages)):
    if ages['medcond_yn'][i] == 'No':
        ages['No'][i] = 1
    else:
        ages['No'][i] = 0
        
    if ages['medcond_yn'][i] == 'Yes':
        ages['Yes'][i] = 1
    else:
        ages['Yes'][i] = 0
        
    if ages['medcond_yn'][i] == 'Unknown or Missing':
        ages['Unknown or Missing'][i] = 1
    else:
        ages['Unknown or Missing'][i] = 0   

age_chart = alt.Chart(ages).mark_bar().encode(
    x='sum(Yes)',
    y='age_group',
    color = 'sex'
)

st.write("""

	The count of records of different age groups

	""")

st.altair_chart(age_chart)
