{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Covid19-Analysis.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyPkHZjtIOxNMEmRO3Xq0zEv"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Asma-0101/Covid19-Analysis/blob/master/Covid19_Analysis.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mZmqRfo-zlZe",
        "colab_type": "text"
      },
      "source": [
        "import required modules"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "I6HbwXe9zcpU",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import seaborn as sns"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Tpojuzr6zxCW",
        "colab_type": "text"
      },
      "source": [
        "Read & edit Covid-19 dataset"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "DDA0hdj5z-BE",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "@st.cache\n",
        "def covid():\n",
        "    covid = pd.read_csv(\"time_series_covid19_confirmed_global.csv\")\n",
        "    covid_agg = covid.groupby(\"Country/Region\").sum()\n",
        "    covid_agg.drop(['Lat', 'Long'], axis=1, inplace=True)\n",
        "    covid_agg['Average cases'] = covid_agg.mean(axis=1)\n",
        "    covid_agg.loc['Average cases'] = covid_agg.mean()\n",
        "    covid_data = pd.DataFrame(covid_agg['Average cases'])\n",
        "    return covid_data"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mYA_YHKZ0FC6",
        "colab_type": "text"
      },
      "source": [
        "Read & edit Population dataset"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hQ1l7Xm60WIs",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def pop():\n",
        "    pop = pd.read_csv(\"WPP2019_TotalPopulationBySex.csv\")\n",
        "    pop_agg = pop.groupby(\"Location\").sum()\n",
        "    useless_cols = ['LocID', 'VarID', 'Time', 'PopMale', 'PopFemale', 'MidPeriod', 'PopTotal']\n",
        "    pop_agg.drop(useless_cols, axis=1, inplace=True)\n",
        "    pop_agg.rename(columns={'PopDensity': 'Population Density'}, inplace=True)\n",
        "    return pop_agg"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "X_0mCZOz0E9k",
        "colab_type": "text"
      },
      "source": [
        "Read & edit Temperature dataset"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "cB7AQdWN0f3p",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "@st.cache\n",
        "def temp():\n",
        "    temp = pd.read_csv(\"globallandtemperaturesbymajorcity.csv\")\n",
        "    temp_agg = temp.groupby(\"country\").sum()\n",
        "    temp_agg.drop(['averagetemperatureuncertainty'], axis=1, inplace=True)\n",
        "    temp_agg.rename(columns={'averagetemperature': 'Average Temperature'}, inplace=True)\n",
        "    return temp_agg"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "l2nkopEh0lp_",
        "colab_type": "text"
      },
      "source": [
        "Join the three datasets to create a new dataframe"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "33HrH59y0tTK",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "data0 = covid().join(pop(), how='inner')\n",
        "data1 = data0.join(temp(), how='inner')"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "N_qtHXrC0zOa",
        "colab_type": "text"
      },
      "source": [
        "Creation of Streamlit pages, adding texts & widgets, plotting graph using seaborn and displaying dataframe"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "78DXhAcF1zna",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def main():\n",
        "    page = st.sidebar.selectbox(\"Choose a page\", ['Analysis', 'About'])\n",
        "    if page == \"Analysis\":\n",
        "        st.title(\"\"\"Covid-19 Analysis\n",
        "                     Based on global climate and population\"\"\")\n",
        "        parameter = st.selectbox(\n",
        "        \"Choose a parameter\", list(data1.columns.values[1:]))\n",
        "\n",
        "        x = data1['Average cases']\n",
        "        y = data1[parameter]\n",
        "        sns.regplot(x, y)\n",
        "        st.pyplot()\n",
        "\n",
        "        if st.checkbox('Show Dataframe'):\n",
        "            display = pd.DataFrame(data1)\n",
        "            display[['Average cases', parameter]]\n",
        "\n",
        "    elif page == 'About':\n",
        "        st.title(\"About\")\n",
        "        st.subheader('Author')\n",
        "        st.write('This project was created by Asma Khan.')\n",
        "        st.subheader('Datasets')\n",
        "        st.write(\"Following provides the sources of datasets used in this project:\")\n",
        "        st.write(\"[Covid-19 dataset](https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases)\")\n",
        "        st.write(\"[Global Population dataset](https://population.un.org/wpp/Download/Standard/CSV/)\")\n",
        "        st.write(\"[Temperature dataset](https://datacatalog.worldbank.org/dataset/climate-change-knowledge-portal-historical-data)\")\n",
        "        st.subheader('Source code')\n",
        "        st.write('https://github.com/Asma-0101/Covid19-Analysis')\n",
        "\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    main()"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}
