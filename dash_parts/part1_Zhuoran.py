import pandas as pd
import streamlit as st
import altair as alt

session = st.sidebar.selectbox("Which session to Look at?", ["Overview", "xxx", "xxxx"])
st.title('COVID-19 in the US')

if session == "Overview":
    import datetime
    from sodapy import Socrata

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
    from vega_datasets import data

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

    st.subheader('Overview of cases in map')
    st.altair_chart(output3, use_container_width=True)

    with st.beta_expander("See explanation"):
        st.write("""
             The percentage change was calculated by.
         """)

