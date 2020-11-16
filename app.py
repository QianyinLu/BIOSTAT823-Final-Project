import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import datetime
import plotly.express as px
import warnings
import math
from sodapy import Socrata
from vega_datasets import data

warnings.simplefilter("ignore")

session = st.sidebar.selectbox("Which session to Look at?", 
                               ["Overview", 
                                "State Level Comparison", 
                                "Case Level Prediction", 
                                "Individual Level Analysis"])

if session == "Overview":
    st.title('Part I: COVID-19 in the US')
    client = Socrata("data.cdc.gov", None)
    results = client.get("9mfq-cb36", limit=200000)
    df1 = pd.DataFrame.from_records(results)
    #df1 = pd.read_csv('data/data/covid_19.csv', index_col=0)
    df1["submission_date"] = df1["submission_date"].astype("datetime64")
    df1 = df1.iloc[:, :6]

    # sidebar
    st.sidebar.subheader("Overview")
    date_range = st.sidebar.slider('Select a range of date',
                                   min(df1.submission_date).date(), max(df1.submission_date).date(),
                                   value=(datetime.date(2020, 4, 22), datetime.date(2020, 7, 22)))
    s = st.sidebar.selectbox(
        "Choose a state from the following List",
        df1.state.unique().tolist()
    )
    s2 = st.sidebar.selectbox(
        "Choose a data type from the following List to show in the map",
        ['Total cases', 'New daily cases', 'Cases per million people', 'Death per million people']
    )

    min_date = pd.Timestamp(datetime.datetime.combine(date_range[0], datetime.datetime.min.time()))
    max_date = pd.Timestamp(datetime.datetime.combine(date_range[1], datetime.datetime.min.time()))
    mask = (df1['submission_date'] > min_date) & (df1['submission_date'] <= max_date)
    dfs = df1[mask & (df1.state == s)]
    dfs = (dfs.assign(new_case_rolling=dfs[['new_case']].rolling(window=7, min_periods=1).mean()).
           assign(new_death_rolling=dfs[['new_death']].rolling(window=7, min_periods=1).mean())
           )

    col1, col2 = st.beta_columns(2)

    with col1:
        # graph:refer to https://altair-viz.github.io/gallery/multiline_tooltip.html
        source = dfs
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['submission_date'], empty='none')

        # The basic line

        base = alt.Chart(source).encode(
            x=alt.X('monthdate(submission_date):O', title='Date')
        )

        bar = base.mark_bar().encode(y=alt.Y('new_case:Q', title='Number of cases'))

        line = base.mark_line(color='red').encode(
            y='new_case_rolling:Q'
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='monthdate(submission_date):O',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=15, dy=-15).encode(
            text=alt.condition(nearest, 'new_case:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='monthdate(submission_date):O',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        output1 = alt.layer(
            bar, line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        )

        # show graph
        st.subheader('Overview of new cases')
        st.altair_chart(output1, use_container_width=True)

    with col2:
        # graph:refer to https://altair-viz.github.io/gallery/multiline_tooltip.html
        source = dfs
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['submission_date'], empty='none')

        # The basic line

        base = alt.Chart(source).encode(
            x=alt.X('monthdate(submission_date):O', title='Date')
        )

        bar = base.mark_bar().encode(y=alt.Y('new_death:Q', title='Number of cases'))

        line = base.mark_line(color='red').encode(
            y='new_death_rolling:Q'
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='monthdate(submission_date):O',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=15, dy=-15).encode(
            text=alt.condition(nearest, 'new_death:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='monthdate(submission_date):O',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        output2 = alt.layer(
            bar, line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        )

        # show graph
        st.subheader('Overview of new death')
        st.altair_chart(output2, use_container_width=True)

    # map plot
    stateid = pd.read_csv('data/data/stateid.csv')
    stateid.columns = ['id', 'State', 'Abbreviation', 'Alpha code']
    state_demo = pd.read_csv('data/data/state_demographic.csv')
    state_demo.columns = ['state', 'Density', 'Under 18', 'Over 65', 'Population', 'male',
                          'female', 'white', 'black', 'indian(Native)', 'asian', 'hawaiian', 'other']

    dfa = df1[df1.submission_date == max(df1.submission_date)]
    dfa = dfa.merge(stateid, how='inner', left_on='state', right_on='Alpha code')
    dfa = dfa.merge(state_demo, how='inner', left_on='state', right_on='state')

    dfa["tot_cases"] = dfa["tot_cases"].astype("int64")
    dfa["new_case"] = dfa["new_case"].astype("float64")
    dfa["tot_death"] = dfa["tot_death"].astype("int64")
    dfa["new_death"] = dfa["new_death"].astype("float64")

    dfa = dfa.assign(Cases_per_m=1000000 * dfa['tot_cases'] / dfa['Population']).assign(
        Death_per_m=1000000 * dfa['tot_death'] / dfa['Population'])
    dfa["Cases_per_m"] = dfa["Cases_per_m"].astype("int64")
    dfa["Death_per_m"] = dfa["Death_per_m"].astype("int64")

    dfa.columns = ['submission_date', 'state', 'total cases', 'new cases', 'total death',
                   'new death', 'id', 'State', 'Abbreviation', 'Alpha code', 'Density',
                   'Under 18', 'Over 65', 'Population', 'male', 'female', 'white', 'black',
                   'indian(Native)', 'asian', 'hawaiian', 'other', 'Cases per million',
                   'Death per million']

    states = alt.topo_feature(data.us_10m.url, 'states')
    source2 = dfa

    if s2 == 'Total cases':
        map1 = alt.Chart(source2).mark_geoshape().encode(
            shape='geo:G',
            color='total cases:Q',
            tooltip=['State', 'total cases:Q', 'total death:Q'])
    elif s2 == 'New daily cases':
        map1 = alt.Chart(source2).mark_geoshape().encode(
            shape='geo:G',
            color='new cases:Q',
            tooltip=['State', 'new cases:Q', 'new death:Q'])
    elif s2 == 'Cases per million people':
        map1 = alt.Chart(source2).mark_geoshape().encode(
            shape='geo:G',
            color='Cases per million:Q',
            tooltip=['State', 'Cases per million:Q', 'Population:Q'])
    else:
        map1 = alt.Chart(source2).mark_geoshape().encode(
            shape='geo:G',
            color='Death per million:Q',
            tooltip=['State', 'Death per million:Q', 'Population:Q'])

    output3 = map1.transform_lookup(
        lookup='id',
        from_=alt.LookupData(data=states, key='id'),
        as_='geo'
    ).properties(
        width=300,
        height=175,
    ).project(
        type='albersUsa'
    )

    st.write('**Overview of cases in map at**',max(df1.submission_date).date())
    st.altair_chart(output3, use_container_width=True)

    with st.beta_expander("About the data source"):
        st.write("""
             The data are updated in real time from the [CDC](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36) of US.
             And you can find the information of its API for python [here](https://dev.socrata.com/foundry/data.cdc.gov/9mfq-cb36).
             This part was quoted from the CDC website:
             >This aggregate dataset is structured to include daily numbers of confirmed and probable case and deaths reported to CDC by states over time. Because these provisional counts are subject to change, including updates to data reported previously, adjustments can occur. These adjustments can result in fewer total numbers of cases and deaths compared with the previous data, which means that new numbers of cases or deaths can include **negative** values that reflect such adjustments
             
         """)

    

elif session == "State Level Comparison":
    st.title('Part II: Policy Comparison on State Level')
    st.sidebar.subheader("State Level Comparison")

    def filt(df, policy, how, var, top=5):
        tmp = df.loc[df['policy']==policy, ['state']+var].sort_values(by=var[2]).reset_index(drop=True)
        if how == "best":
            return tmp[:top]
        else:
            return tmp[-top:].iloc[::-1].reset_index(drop=True)
    compare = pd.read_csv("data/data/compare.csv")
    policy = st.sidebar.selectbox(
        "Choose a policy from the following List",
        compare.policy.unique().tolist())
    day = st.sidebar.selectbox("Choose a day range for analysis", [7, 15])
    top = st.sidebar.slider(
        "How many state you want to see in the bar plots?", 5, 10, 5)

    var = ["before_7", "after_7", "diff_7"] if day == 7 else ["before_15", "after_15", "diff_15"]
    best = filt(compare, policy, "best", var, top)
    worst = filt(compare, policy, "worst", var, top)

    col1, col2 = st.beta_columns(2)

    with col1:
        base = alt.Chart(best).encode(x = alt.X('state', title='State', sort=None))
        bar1 = base.mark_bar().encode(y=alt.Y(var[2], title='Difference of Increase Rate'),
                                      tooltip = ['state']+var)
        st.subheader(str(top)+' states that \"'+policy+'\" performs best')
        st.altair_chart(bar1, use_container_width=True)
    
    with col2:
        base = alt.Chart(worst).encode(x = alt.X('state', title='State', sort=None))
        bar2 = base.mark_bar().encode(y=alt.Y(var[2], title='Difference of Increase Rate'),
                                      tooltip = ['state']+var)
        st.subheader(str(top)+' states that \"'+policy+'\" performs worst')
        st.altair_chart(bar2, use_container_width=True)
    
    with st.beta_expander("Model Explaination"):
        st.write("""
             This model compares the average increase rate of total cases on each state 7/15 days before and after the implementation date of the certain policy. 7 days represents short term while 15 days represents long term. The average accuracy is computed by
         """)
        st.latex(r"""
                    r_{average}=(\prod_{i=1}^{K}(1+r_i))^{\frac{1}{K}}-1
                    """)
    
    client = Socrata("data.cdc.gov", None)
    results = client.get("9mfq-cb36", limit=200000)
    df = pd.DataFrame.from_records(results)

    df["submission_date"] = df["submission_date"].astype("datetime64")
    df['tot_cases'] = df['tot_cases'].astype(int)
    df['new_case'] = df['new_case'].astype(float)
    df = df.loc[:, ["submission_date", "state", "tot_cases", "new_case"]]
    df["lag_date"] = df["submission_date"].shift(1)
    join = pd.merge(df, df, how="left", left_on = ["submission_date", "state"], right_on = ["lag_date", "state"])
    join["inc_rate"] = join["new_case_y"] / join["tot_cases_x"] 
    join = join.fillna(0)

    def helper1(state):
        tmp = join[join["state"] == state].reset_index(drop=True)
        inf_ind = np.where(tmp.inc_rate==math.inf)[0]
        return tmp.loc[inf_ind[0]+1:, ["submission_date_x", "state", "inc_rate"]] if inf_ind else tmp.loc[:, ["submission_date_x", "state", "inc_rate"]]

    df_ = pd.concat([helper1(x) for x in np.unique(join["state"])],axis=0).reset_index(drop=True)
    df_.columns = ["date", "state", "inc_rate"]
    total = df.groupby("submission_date", as_index=False)[["tot_cases", "new_case"]].sum()
    total["lag_date"] = total["submission_date"].shift(1)
    total_ = pd.merge(total, total, how="left", left_on = "submission_date", right_on = "lag_date")
    total_["inc_rate"] = total_["new_case_y"] / total_["tot_cases_x"] 
    total_ = total_[["submission_date_x", "inc_rate"]].dropna()
    total_.columns = ["date", "total_inc_rate"]

    case = pd.read_csv("data/data/covid_19.csv")
    case["submission_date"] = case["submission_date"].astype("datetime64")
    case = case.loc[:, ["submission_date", "state", "tot_cases", "new_case"]]
    case["lag_date"] = case["submission_date"].shift(1)
    join = pd.merge(case, case, how="left", left_on = ["submission_date", "state"], right_on = ["lag_date", "state"])
    join["inc_rate"] = join["new_case_y"] / join["tot_cases_x"] 
    join = join.fillna(0)
    case_ = pd.concat([helper1(x) for x in np.unique(join["state"])],axis=0).reset_index(drop=True)
    case_.columns = ["date", "state", "inc_rate"]

    df2 = pd.merge(case_, total_, on="date", how="left")
    df2["diff"] = df2["inc_rate"] - df2["total_inc_rate"]
    df2.columns = ["date", 'state', "increase rate in state", "increase rate in US", "difference"]

    df2[["increase rate in state", "increase rate in US", "difference"]] = df2[["increase rate in state", "increase rate in US", "difference"]].round(4)
    
    stateid = pd.read_csv('data/data/stateid.csv')
    stateid.columns = ['id', 'State', 'Abbreviation', 'Alpha code']

    df2 = df2.merge(stateid, how='inner', left_on='state', right_on='Alpha code')

    date = st.sidebar.slider('Select a day you want to check on the map',
                             min(df2.date).date(), max(df2.date).date(),
                             value=datetime.date(2020, 4, 22))

    states = alt.topo_feature(data.us_10m.url, 'states')
    source2 = df2[df2["date"] == pd.Timestamp(datetime.datetime.combine(date, datetime.datetime.min.time()))]
    map1 = alt.Chart(source2).mark_geoshape().encode(
                shape='geo:G',
                color='difference',
                tooltip=['state', "increase rate in state", "increase rate in US", "difference"])
    output3 = map1.transform_lookup(
            lookup='id',
            from_=alt.LookupData(data=states, key='id'),
            as_='geo'
            ).properties(
                width=300,
                height=175,
                ).project(
                    type='albersUsa'
                    )

    st.subheader('Relative Increase Rate in map')
    st.altair_chart(output3, use_container_width=True)
    
    with st.beta_expander("About the data source"):
        st.write("""
             The data are updated in real time from the [CDC](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36) of US.
             And you can find the information of its API for python [here](https://dev.socrata.com/foundry/data.cdc.gov/9mfq-cb36).
             This part was quoted from the CDC website:
             >This aggregate dataset is structured to include daily numbers of confirmed and probable case and deaths reported to CDC by states over time. Because these provisional counts are subject to change, including updates to data reported previously, adjustments can occur. These adjustments can result in fewer total numbers of cases and deaths compared with the previous data, which means that new numbers of cases or deaths can include **negative** values that reflect such adjustments
         """)
    
elif session == "Case Level Prediction":
    
    st.title('Part III: Predict Covid19 Case Growth Rate')
    st.sidebar.subheader("Case Level Prediction")
    level = st.sidebar.selectbox("", ["Overview", "State Level"])
    importance = pd.read_csv("data/data/importance.csv", index_col = 0)
    importance = importance[~importance.varname.str.contains("lag")]
    importance = importance[importance.importance>0]
    pred = pd.read_csv("data/data/pred.csv", index_col = 0)
    res = pd.read_csv("data/data/res.csv", index_col = 0)
    res = res.round(4)
    demo = pd.read_csv("data/data/state_demographic.csv")

    if level == "Overview":
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
            
    if level == "State Level":
    
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
            
elif session == "Individual Level Analysis":
    st.title('Part IV: Individual Level Analysis')
    st.sidebar.subheader("Individual Level Analysis")
    selection = st.sidebar.radio("Go to", ["Introduction", "Visualization"])

    if selection == "Introduction":
        st.subheader('COVID-19 (Population Data)')
        st.write("""
                 In this part we decided to explore the relationship between the Covid-19 death/infection data and the population data. The original data is COVID-19 Case Surveillance Public Use Data collected by CDC. Population data include race, age as well as gender information. However, the original dataset is huge (over 1,500,000 individual observations) and is sorted by age groups (from 0-9 years to over 80 years). Considering the runtime of Streamlit, we have to sample from the original data. However, we cannot choose randomly or just slice one part of the data, since people in different age groups take different proportion of total population. We decided to take 5 percent of original data for each age group. The composition of the original data is:
                 """)
        st.image('img/tree2.png',use_column_width=True)
        st.write("""
             After the sampling 5 percent of each age group, the proportion of each age groups still maintain the same as the original data:
            """)
        st.image('img/tree.png',use_column_width=True)
        st.write("""
             The visualization of the sample data should have a similar outcome as the visualization of the original data. Other variables such as race and gender is distributed randomly, therefore the sampling process based on age group should not have a major impact on them.
             
             Source of Data: https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf
             """)
    if selection == "Visualization":
        alt.data_transformers.disable_max_rows()

        ind = pd.read_csv('data/data/individual_new.csv').iloc[:,1:]
        ind = ind.replace('Unknown','Unknown or Missing')
        ind = ind.replace('Missing','Unknown or Missing')
        ind = ind.replace('NA','Unknown or Missing')
        ind = ind.replace('nan','Unknown or Missing')
        ind = ind.replace(np.nan,'Unknown or Missing')

        ind['pop_race'] = ind['race'].map(ind['race'].value_counts()) 
        ind['density_race'] = 1/ind['pop_race']
        ind['pop_age'] = ind['age_group'].map(ind['age_group'].value_counts()) 
        ind['density_age'] = 1/ind['pop_age']

        session = st.sidebar.selectbox("Which parameter? ", ["Race", "Age Group"])
        st.subheader('COVID-19 (Population Data)')
        if session == "Race":
            choice = st.selectbox("Rate", ["Infection Case", "Fatality Case"])
            if choice == "Fatality Case":
                base_f = alt.Chart(ind[(ind['death_yn'] == 'Yes') & (ind['sex'] =='Female')]).encode(
                alt.X('race', axis=alt.Axis(title="Female")))

                histogram_f = base_f.mark_bar().encode(
                    alt.Y('count(death_yn):Q',axis=alt.Axis(title='total death count', titleColor='#5276A7')),
                    color = 'race')

                point_f = base_f.mark_line(point=True).encode(
                    alt.Y('sum(density_race):O',axis=alt.Axis(title='average death rate', titleColor='#57A44C')))

                layer_f = alt.layer(histogram_f, point_f).resolve_scale(y = 'independent').properties(width=200,height = 400)
                base_m = alt.Chart(ind[(ind['death_yn'] == 'Yes') & (ind['sex'] =='Male')]).encode(
                alt.X('race', axis=alt.Axis(title="Male")))

                histogram_m = base_m.mark_bar().encode(
                    alt.Y('count(death_yn):Q',axis=alt.Axis(title='total death count', titleColor='#5276A7')),
                    color = 'race')

                point_m = base_m.mark_line(point=True).encode(
                    alt.Y('sum(density_race):O',axis=alt.Axis(title='average death rate', titleColor='#57A44C')))

                layer_m = alt.layer(histogram_m, point_m).resolve_scale(y = 'independent').properties(width=200,height = 400)
                f = layer_f | layer_m
                st.altair_chart(f)

                with st.beta_expander("See Detail"):
                    st.write("""
                    Out of 74996 individuals, White/Non-Hispanic as well as Black/Non-Hispanic, therefore they have the largest death count. There is no obvious differnece between male and female for
                    most of the races except for Hispanic/Latino that male has a much bigger death count than female. 
                 """)

            if choice == "Infection Case":
                base_f = alt.Chart(ind[(ind['medcond_yn'] == 'Yes') & (ind['sex'] =='Female')]).encode(
                alt.X('race', axis=alt.Axis(title="Female")))

                histogram_f = base_f.mark_bar().encode(
                    alt.Y('count(medcond_yn):Q',axis=alt.Axis(title='total death count', titleColor='#5276A7')),
                    color = 'race')

                point_f = base_f.mark_line(point=True).encode(
                    alt.Y('sum(density_race):O',axis=alt.Axis(title='average death rate', titleColor='#57A44C')))

                layer_f = alt.layer(histogram_f, point_f).resolve_scale(y = 'independent').properties(width=200,height = 400)
                base_m = alt.Chart(ind[(ind['medcond_yn'] == 'Yes') & (ind['sex'] =='Male')]).encode(
                alt.X('race', axis=alt.Axis(title="Male")))

                histogram_m = base_m.mark_bar().encode(
                    alt.Y('count(medcond_yn):Q',axis=alt.Axis(title='total infection count', titleColor='#5276A7')),
                    color = 'race')

                point_m = base_m.mark_line(point=True).encode(
                    alt.Y('sum(density_race):O',axis=alt.Axis(title='average infection rate', titleColor='#57A44C')))
                layer_m = alt.layer(histogram_m, point_m).resolve_scale(y = 'independent').properties(width=200,height = 400)
                f = layer_f | layer_m
                st.altair_chart(f)
                with st.beta_expander("See Detail"):
                    st.write("""
                    Out of 74996 individuals, White/Non-Hispanic as well as Black/Non-Hispanic, therefore they have the largest death count. There is no obvious differnece between male and female for
                    most of the races except for Hispanic/Latino that male has a much bigger death count than female.   
                 """)
        age = ind[['sex','age_group','death_yn','medcond_yn','density_age','pop_age']]

        if session == "Age Group":
            choice = st.selectbox("Rate", ["Infection Case", "Fatality Case"])
            if choice == "Fatality Case":
                base = alt.Chart(age[(age['sex'] != 'Other') & (age['death_yn'] == 'Yes')]).encode(
                alt.X('age_group', axis=alt.Axis(title=None)))

                histogram = base.mark_bar().encode(
                alt.Y('count(death_yn)',axis=alt.Axis(title='total death count', titleColor='#5276A7')),
                color = 'sex')

                point = base.mark_line(point=True).encode(
                alt.Y('sum(density_age)',axis=alt.Axis(title='average death rate', titleColor='#57A44C')),color = 'sex')

                layer = alt.layer(histogram,point).resolve_scale(y = 'independent').properties(width=500,height = 600)
                st.write("""
                The count of records of different age groups
                """)
                st.altair_chart(layer)

                with st.beta_expander("See Detail"):
                    st.write("""
                    Out of 74996 individuals, White/Non-Hispanic as well as Black/Non-Hispanic, therefore they have the largest death count. There is no obvious differnece between male and female for
                    most of the races except for Hispanic/Latino that male has a much bigger death count than female. 
                 """)
            if choice == "Infection Case":
                base = alt.Chart(age[(age['sex'] != 'Other') & (age['medcond_yn'] == 'Yes')]).encode(
                alt.X('age_group', axis=alt.Axis(title=None)))

                histogram = base.mark_bar().encode(
                alt.Y('count(medcond_yn)',axis=alt.Axis(title='total death count', titleColor='#5276A7')),
                color = 'sex')

                point = base.mark_line(point=True).encode(
                alt.Y('sum(density_age)',axis=alt.Axis(title='average death rate', titleColor='#57A44C')),color = 'sex')

                layer = alt.layer(histogram,point).resolve_scale(y = 'independent').properties(width=500,height = 600)
                st.write("""
                The count of records of different age groups

                """)
                st.altair_chart(layer)
                with st.beta_expander("See Detail"):
                    st.write("""
                    Out of 74996 individuals, White/Non-Hispanic as well as Black/Non-Hispanic, therefore they have the largest death count. There is no obvious differnece between male and female for
                    most of the races except for Hispanic/Latino that male has a much bigger death count than female.
                 """)