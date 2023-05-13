import streamlit as st
import pandas as pd
import seaborn as sns


@st.cache
def covid():
    covid = pd.read_csv("time_series_covid19_confirmed_global.csv")
    covid_agg = covid.groupby("Country/Region").mean()
    covid_agg.drop(['Lat', 'Long'], axis=1, inplace=True)
    covid_agg['Average cases'] = covid_agg.mean(axis=1)
    covid_agg.loc['Average cases'] = covid_agg.mean()
    covid_data = pd.DataFrame(covid_agg['Average cases'])
    return covid_data


def pop():
    pop = pd.read_csv("WPP2019_TotalPopulationBySex.csv")
    pop_agg = pop.groupby("Location").mean()
    useless_cols = ['LocID', 'VarID', 'Time', 'PopMale', 'PopFemale', 'MidPeriod', 'PopTotal']
    pop_agg.drop(useless_cols, axis=1, inplace=True)
    pop_agg.rename(columns={'PopDensity': 'Population Density'}, inplace=True)
    return pop_agg


@st.cache
def temp():
    temp = pd.read_csv("globallandtemperaturesbymajorcity.csv")
    temp_agg = temp.groupby("country").mean()
    temp_agg.drop(['averagetemperatureuncertainty'], axis=1, inplace=True)
    temp_agg.rename(columns={'averagetemperature': 'Average Temperature'}, inplace=True)
    return temp_agg


data0 = covid().join(pop(), how='inner')
data1 = data0.join(temp(), how='inner')


def main():
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    page = st.sidebar.selectbox("Choose a page", ['Analysis', 'About'])
    if page == "Analysis":
        st.title("""Covid-19 Analysis""")
        st.write('Based on global climate and population. The application is currently being upgraded. The new version would be launched soon')
        parameter = st.selectbox(
        "Choose a parameter", list(data1.columns.values[1:]))

        x = data1['Average cases']
        y = data1[parameter]
        sns.regplot(x, y)
        st.pyplot()

        if st.checkbox('Show Dataframe'):
            display = pd.DataFrame(data1)
            display[['Average cases', parameter]]

    elif page == 'About':
        st.title("About")
        st.subheader('Author')
        st.write('Hi, I am Asma Khan, majoring in Information Technology from Mumbai-India. Connect with me on LinkedIn: https://www.linkedin.com/in/asma-khan-0676a116a/.')
        st.subheader('About the application')
        st.write('This application is developed to make a comparative study between basic characteristics of various countries and the average cases in those countries. The sources of the datasets have been mentioned below.')
        st.subheader('Datasets')
        st.write("Following provides the sources of datasets used in this project:")
        st.write("[Covid-19 dataset](https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases)")
        st.write("[Global Population dataset](https://population.un.org/wpp/Download/Standard/CSV/)")
        st.write("[Temperature dataset](https://datacatalog.worldbank.org/dataset/climate-change-knowledge-portal-historical-data)")
        st.subheader('Source code')
        st.write('https://github.com/Asma-0101/Covid19-Analysis')
        st.subheader('Disclaimer')
        st.write('Evidently this project is solely for the purpose of studying basic usage of Python with Streamlit and it contains no profound meaning to it.')

        
if __name__ == '__main__':
    main()
