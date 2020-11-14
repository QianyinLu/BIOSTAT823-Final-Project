import pandas as pd
import streamlit as st
import altair as alt
import datetime
import plotly.express as px

st.title('Part I: Predict Covid19 Case Growth Rate')
session = st.sidebar.selectbox("Which session to Look at?", ["Overview", "State Level"])
importance = pd.read_csv("importance.csv", index_col = 0)
importance = importance[~importance.varname.str.contains("lag")]
importance = importance[importance.importance>0]
pred = pd.read_csv("pred.csv", index_col = 0)
res = pd.read_csv("res.csv", index_col = 0)
res = res.round(4)
demo = pd.read_csv("demographic.csv", index_col= 0)


if session == "Overview":
    US = importance[importance.state =="all"]
    #Sidebar
    st.sidebar.subheader("Select Number of Features")
    top_num = st.sidebar.number_input("How many top features to look at(Max 24):", 1, 24, 24)
  
    st.header("Covid19 Case Growth - US")

    #error
    st.subheader("Prediction Error")
    res_us = res[res.state == "all"]
    us_err_train = "Training Error:  " + str(float(res_us["train_err"].values))
    us_err_test = "Test Error:  " + str(float(res_us["test_err"].values))
    st.write(us_err_train)
    st.write(us_err_test)
    
    #plot
    st.subheader("Feature Importance")
    US_filtered = US.sort_values("importance", ascending = False).head(top_num)
    US_plot = alt.Chart(US_filtered).mark_bar().encode(
                    y=alt.Y('varname:N', sort = '-x'),
                    color='varname:N',
                    x=alt.X('importance:Q', axis=alt.Axis(labels=False, title = 'importance level'))
              )
    st.altair_chart(US_plot, use_container_width = True)
    with st.beta_expander("See Variable explanation"):
         st.write("""
             **Density**: Density within each state  
             **ICUBedsOccAnyPat__N_ICUBeds_Est**:  ICU bed occupancy, percent estimate (percent of ICU beds)        
             **InBedsOccAnyPat_Numbeds_Est**: Hospital inpatient bed occupancy, percent estimate (percent of inpatient beds)     
             **InBedsOccCOVID_Numbeds_Est**: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, percent estimate (percent of inpatient beds)      
             **Log_ICUBeds_Occ_AnyPat_Est**: ICU bed occupancy, estimate, log    
             **Log_ICUBeds_Occ_AnyPat_Est_Avail**: ICU beds available, estimate, log     
             **Log_InpatBeds_Occ_AnyPat_Est**: Hospital inpatient bed occupancy, estimate, log     
             **Log_InpatBeds_Occ_AnyPat_Est_Avail**: Hospital inpatient beds available, estimate, log    
             **Log_InpatBeds_Occ_COVID_Est**: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, estimate, log    
             **Over 65**: Percentage of over 65 years old population within the state  
             **Population**: Total population within the state  
             **Under 18**: Percentage of under 18 population within the state 
             **asian**: Percentage of Asian population within the state  
             **black**: Percentage of African American population within the state    
             **business closed**: Whether a state is under a period that closed non-essential businesses statewide  
             **face mask fine**: Whether a face mask mandate is enforced through fines     
             **face mask mandatory**: Whether a state is under a period that mandated face mask use in public spaces by all individuals statewide.  
             **hawaiian**: Percentage of Hawaiian population within the state  
             **Indian(Native)**: Percentage of Indian(Population) population within the state  
             **religious gathering forbidden**: Whether a state exempted religious gatherings from social distancing mandates  
             **restaurants closed**: Whether a state is under the period that closed all restaurants (except for takeout)  
             **sex**: The percentage of Male within the state   
             **stay at home order**: Whether a state is under the period that state's stay at home/shelter in place order went into effect  
             **white**: Percentage of White population within the state  
         """)
            
    with st.beta_expander("See Model explanation"):
         st.write("""   
                  We built a random forest model to predict the daily increase rate of total cases. The predictor includes four parts: lag variable (not included in the plot), hospitalization, policy and demographic data. The data range is from 2020 April to July and our data was collected from the state level. For this part, we used a single model for the entire United States.
                  """)
    
    st.header("Data Source")
    st.write(""" 
    1. [Hospitalization](https://www.cdc.gov/nhsn/covid19/report-patient-impact.html#anchor_1594393649)       
    2. [Demographic](https://www.census.gov/data/developers/data-sets/acs-1year.html)    
    3. [Policy](https://github.com/USCOVIDpolicy/COVID-19-US-State-Policy-Database)""")
            
if session == "State Level":
    
    #### predicting
    #sidebar
    st.sidebar.subheader("Pick A State")
    s = st.sidebar.selectbox(
        "Choose a state from the following List",
         list(set(pred.state))
    )
    st.sidebar.subheader("Input a Date Range")
    date_s = st.sidebar.date_input("Put a date range", value = (datetime.date(2020, 4, 1), datetime.date(2020, 7, 7)), 
              min_value = datetime.date(2020, 4, 1), max_value = datetime.date(2020, 7, 1))
    
    
    #preprocess the data
    pred["date"] = pd.to_datetime(pred["date"])
    if len(date_s) != 1:
        date_filter = [i >= date_s[0] and i <= date_s[1] for i in pred.date]
    else:
        date_filter = [i == date_s[0] for i in pred.date]
        st.write("Warning: Please input the end date!(end date and start date can not be the same date)")
    pred_date = pred[date_filter]
    pred_date["date"] = pred_date["date"].dt.strftime("%-m/%-d")
    state = pred_date[pred_date.state == s]
    state = state[["date","inc_rate","inc_rate_pred"]]
    state.columns = ["date","Actual Growth Rate","Predicted Growth Rate"]
    source = state.melt("date", var_name='category', value_name='Y')
    
    header_state = "STATE: " + s
    st.header(header_state)

    #error
    st.subheader("Prediction Error")
    sta_us = res[res.state == s]
    sta_err_train = "Training Error:  " + str(float(sta_us["train_err"].values))
    sta_err_test = "Test Error:  " + str(float(sta_us["test_err"].values))
    st.write(sta_err_train)
    st.write(sta_err_test)
    
    #plot predicted growth
    st.subheader("Predicted VS Actual Case Growth Rate")
    
    if state.shape[0]<12:
        skip_num = 1
    else:
        skip_num = round(state.shape[0]/12)
    
    state_prediction = px.line(source, x="date", y="Y", color='category')
    state_prediction.update_layout(
        xaxis = dict(
        dtick = skip_num
        )
    )
    st.plotly_chart(state_prediction)
    
    
    #### feature importance 
    state_feature = importance[importance.state == s]
    
    #sidebar
    st.sidebar.subheader("Select Number of Features")
    state_feature_num = st.sidebar.number_input("How many top features to look at:", 1, state_feature.shape[0], 
                                                state_feature.shape[0])
    
    #plot feature importance 
    st.subheader("Feature Importance")
    state_feature = state_feature.sort_values("importance", ascending = False).head(state_feature_num)
    state_imp = alt.Chart(state_feature).mark_bar().encode(
                    y=alt.Y('varname:N', sort = '-x'),
                    color='varname:N',
                    x=alt.X('importance:Q', axis=alt.Axis(labels=False, title = 'importance level'))
              )
    st.altair_chart(state_imp, use_container_width = True)
    
    with st.beta_expander("See Model explanation"):
         st.write("""   
                  We built a random forest model to predict the daily increase rate of total cases for each state. The predictor includes four parts: lag variable (not included in the plot), hospitalization, and policy. Notice that we did not include demographic data because such data should all be the same within the state. The data range is from 2020 April to July and our data was collected from the state level. For this part, we used different model (adjusting parameters) for different states.
                  """)
            
    #### state specific
    st.subheader("State Information")
    demo["other"] = 100 - demo["white"] - demo["black"] - demo["indian(Native)"] - demo["asian"] - demo["hawaiian"] 
    demo.columns = ['State', 'Density', 'Under 18', 'Over 65', 'Population', 'Male',
       'Female', 'White', 'Black', 'Indian(Native)', 'Asian', 'Hawaiian',
       'Other']
    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
    }
    state_abv = []
    for i in demo.State:
        state_abv.append(us_state_abbrev[i])
    demo["State"] = state_abv
    demo_filtered = demo[demo.State == s]
    
    
    
    gender = demo_filtered[["State","Male","Female"]]
    gender = gender.melt("State", var_name='Sex', value_name='Percentage')
    gender_plot = px.pie(gender, values='Percentage', names='Sex', color_discrete_sequence = ["pink","green"],title = "Sex Ratio")
    st.plotly_chart(gender_plot,use_container_width = True)
    
    race = demo_filtered[["State","White", "Black", "Indian(Native)", "Asian", "Hawaiian", "Other"]]
    race = race.melt("State", var_name='Race', value_name='Percentage')
    race_plot = px.pie(race, values='Percentage', names='Race', 
                       color_discrete_sequence = ["lightblue","green","pink","teal","coral","brown"],title = "Race Ratio")
    st.plotly_chart(race_plot,use_container_width = True)

    display = st.checkbox('Show me more data')
    age = demo_filtered[["State", "Under 18", "Over 65"]]
    age = age.melt("State", var_name='Age', value_name='Percentage')
    if display:
        col1, col2 = st.beta_columns([2, 2])
        age_plot = px.bar(age, x='Age', y='Percentage',color="Age", color_discrete_sequence = ["pink","green"],
                         title = "Age Group Ratio")
        col1.plotly_chart(age_plot, use_container_width = True)
        
        col2.subheader("Data Table")
        col2.write(demo_filtered.round(1).T)