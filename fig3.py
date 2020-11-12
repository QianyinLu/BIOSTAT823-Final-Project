
import pandas as pd
import streamlit as st
import altair as alt

session = st.sidebar.selectbox("Which session to Look at?", ["Overview", "xxx", "xxxx"])
st.title('COVID-19 in the US')

if session == "Overview":
    import datetime

    df1 = pd.read_csv('covid_19.csv', index_col=0)
    df1["submission_date"] = df1["submission_date"].astype("datetime64")
    df1 = df1.iloc[:, :6]

    # sidebar
    st.sidebar.subheader("Overview")
    date_range = st.sidebar.slider('Select a range of date',
                                   min(df1.submission_date).date(), max(df1.submission_date).date(),
                                   value=(datetime.date(2020, 5, 22), datetime.date(2020, 6, 22)))
    s = st.sidebar.selectbox(
        "Choose a state from the following List",
        df1.state.unique().tolist()
    )

    min_date = pd.Timestamp(datetime.datetime.combine(date_range[0], datetime.datetime.min.time()))
    max_date = pd.Timestamp(datetime.datetime.combine(date_range[1], datetime.datetime.min.time()))
    mask = (df1['submission_date'] > min_date) & (df1['submission_date'] <= max_date)
    dfs = df1[mask & (df1.state == s)]
    dfs = (dfs.assign(new_case_rolling=dfs[['new_case']].rolling(window=7, min_periods=1).mean()).
           assign(new_death_rolling=dfs[['new_death']].rolling(window=7, min_periods=1).mean())
           )


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
    output = alt.layer(
        bar, line, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )

    # show graph
    st.subheader('Overview of new cases')
    st.altair_chart(output, use_container_width=True)

    with st.beta_expander("See explanation"):
        st.write("""
             The percentage change was calculated by.
         """)

