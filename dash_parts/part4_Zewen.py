import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


st.sidebar.subtitle('Navigation of Covid-19 Population Data')
selection = st.sidebar.radio("Go to", ["Introduction", "Visualization"])

if selection == "Introduction":
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
    st.title('COVID-19 (Population Data)')


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





        







