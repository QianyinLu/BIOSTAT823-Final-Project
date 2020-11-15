import numpy as np
import math
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
import datetime

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
day = st.sidebar.selectbox(
    "Choose a day range for analysis",
    [7, 15])
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
    
from sodapy import Socrata

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