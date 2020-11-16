import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


st.sidebar.subtitle('Navigation of Covid-19 Population Data')
selection = st.sidebar.radio("Go to", ["Introduction", "Visualization"])

if selection == "Introduction":


    st.title('COVID-19 (Population Data)')


    st.write("""
                    The population data we 
                    很多废话
                     
                 """)

    st.image('img/tree2.png',use_column_width=True)



    st.write("""
                    After the sampling
                    继续废话
                     
                 """)
    st.image('img/tree.png',use_column_width=True)




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





        







