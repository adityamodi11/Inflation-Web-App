from numpy import true_divide
import streamlit as st
from streamlit.proto.Progress_pb2 import Progress
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import time
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio

#monthly_price = pd.read_csv('monthly_price.csv')
#state = monthly_price['state'].to_list()
#commodity = monthly_price['commodity'].to_list()

st.sidebar.title("Inflation Analyzer")
st.sidebar.image('inflation.jpg')
st.sidebar.text("-By Aditya Modi")

user_menu = st.sidebar.radio(
    'Select Page',
    ('Home','Analyze','Data')
)

if user_menu == 'Home':
    st.title("Home")
    st.header("Here You will learn Key terms to analyze inflation!")
    st.text("- By Aditya Modi")
    st.image("in.jpg",use_column_width = True)
    st.text("To Skip this, select another Page....")

    st.subheader("Inflation")
    st.write("""Inflation is an economic indicator that indicates the rate of rising prices of goods and services in the economy. 
              Ultimately it shows the decrease in the buying power of the rupee. It is measured as a percentage.This percentage indicates the increase or decrease from the previous period. Inflation can be a cause of concern as
            the value of money keeps decreasing as inflation rises.""")
    st.video("https://youtu.be/beAvFHP4wDI")
    st.subheader("Cause of Inflation")
    st.write("""
    Monetary Policy: It determines the supply of currency in the market. Excess supply 
                                 of money leads to inflation. Hence decreasing the value of the currency.

    Fiscal Policy: It monitors the borrowing and spending of the economy. Higher borrowings (debt),
                           result in increased taxes and additional currency printing to repay the debt.

    Demand-pull Inflation: Increases in prices due to the gap between the demand (higher) and supply (lower).

    Cost-push Inflation: Higher prices of goods and services due to increased cost of production.

    Exchange Rates: Exposure to foreign markets are based on the dollar value. 
                            Fluctuations in the exchange rate have an impact on the rate of inflation. """)

    st.subheader("Consumer Price Index")
    st.write("""The Consumer Price Index (CPI) is a measure that examines the weighted average of prices of a basket of consumer goods and services, such as transportation, food, and medical care. It is calculated by taking price changes for each item in the predetermined basket of goods and averaging them. Changes in the CPI are used to assess price changes associated with the cost of living.
                The CPI is one of the most frequently used statistics for identifying periods of inflation or deflation. It may be compared with the producer price index (PPI), which instead of considering prices paid by consumers looks at what businesses pay for inputs.""")

    st.subheader("Wholesale Price Index")
    st.write("""A wholesale price index (WPI) is an index that measures and tracks the changes in the price of goods in the stages before the retail level. This refers to goods that are sold in bulk and traded between entities or businesses (instead of between consumers). Usually expressed as a ratio or percentage, the WPI shows the included goods'
               average price change; it is often seen as one indicator of a country's level of inflation.""")

    st.subheader("Correlation")
    st.write("""Correlation shows the strength of a relationship between two variables and is expressed numerically by the correlation coefficient. The correlation coefficient's values range between -1.0 and 1.0.
                A perfect positive correlation means that the correlation coefficient is exactly 1. This implies that as one security moves, either up or down, the other security moves in lockstep, in the same direction. A perfect negative correlation means that two assets move in opposite directions, while a zero correlation implies no linear relationship at all.""")
state = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Goa',
       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu Kashmir',
       'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
       'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
       'National Capital', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim',
       'Tamil Nadu', 'Telangana', 'Tripura', 'Union Territories',
       'Uttar Pradesh', 'Uttarakhand', 'West Bengal']


commodity = ['Moong', 'Gram', 'Mustard Oil', 'Onion', 'Potato', 'Ragi',
       'Red Chillies', 'Rice', 'Salt', 'Sugar', 'Suji', 'Tea', 'Apple',
       'Arhar', 'Atta', 'Bajra', 'Banana', 'Besan', 'Biscuit',
       'Groundnut Oil', 'Gur', 'Jowar', 'Maida', 'Maize', 'Masur', 'Meat',
       'Milk', 'Coriander', 'Cummin Seed', 'Eggs', 'Fish', 'Ghee',
       'Gingelly Oil', 'Black Pepper', 'Bread', 'Brinjal', 'Butter',
       'Chicken', 'Coconut', 'Coconut Oil', 'Coffee', 'Tomato',
       'Turmeric', 'Urad', 'Vanaspati', 'Wheat', 'Gents Dhoti', 'Saree',
       'Glycodin', 'Ink', 'Kerosene Oil', 'Kettle', 'Long Cloth',
       'Match Box', 'Pant Cloth', 'Paper', 'Pencil', 'Pent Cloth',
       'Razor Blade', 'Sandals-Ladies', 'Chappal-Rubber',
       'Saridon/Anacin', 'Septran', 'Shirting', 'Shoes-Gents',
       'Soft Cake', 'Tawa', 'Tooth Paste', 'Tooth Powder', 'Torch Cell',
       'Tumbler', 'Vics Vaporub', 'Washing Soap', 'Washing soda',
       'Bathing Soap', 'Burnol', 'Cement', 'Chappal-Ladies', 'Crocin',
       'Cycle Tube', 'Cycle Tyre', 'Detergent Powder', 'Diesel',
       'Electric bulb', 'Exercise Book']


if user_menu == 'Analyze':

    st.header("Select the Credentials")
    col1,col2 = st.columns(2)
    
    a =col1.selectbox("State",state)
    b = col2.selectbox("Product",commodity)
    col3 = st.slider("Year",min_value=2001,max_value=2021,step=1)
    button = st.button("Submit")
    if button:
        st.success("Submitted!")  
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
        
        st.balloons()
        
        st.subheader("Commodity Price Over Years")
        st.plotly_chart(helper.price_comm(a,b))

        st.subheader("Inflation Over Years")
        st.plotly_chart(helper.inflation(a,b))

        # st.subheader("Inflation Over Years")
        st.plotly_chart(helper.inf_df(a,b))

        st.subheader("Diesel & Petrol vs Commodity")
        st.plotly_chart(helper.fuel_economy2(a,b)[0])
        st.write("The Correlation b/w diesel and Commodity Price is ",helper.fuel_economy2(a,b)[1])
        st.plotly_chart(helper.fuel_economy(a,b)[0])
        st.write("The Correlation b/w Petrol and Commodity Price is ",helper.fuel_economy(a,b)[1])


        st.subheader("Price at different States")
        st.text("Expand the map from the top-right corner for better view.")
        st.text("Price(Rs 0) means data is not avaiable for tha region")
        st.plotly_chart(helper.state_wise_price(b,col3))
        st.plotly_chart(helper.state_wise(b,col3))


        st.subheader("State vs State comparison")
        st.plotly_chart(helper.state_comp(b,col3,a))
        st.plotly_chart(helper.state_comp_df(b,col3,a))

        st.subheader("Oil Economy")
        st.plotly_chart(helper.oil_economy())

        st.subheader("Oil Inflation")
        st.plotly_chart(helper.oil_inf())

pet = pd.read_csv("petrol.csv")
die = pd.read_csv("diesel.csv")

if user_menu == 'Data':

    st.title("Data Sets(Sample df)")
    
    st.subheader("Food and Non-Food Retail Price")
    st.markdown(""" You can download the complete data from this [link](https://www.kaggle.com/kk9969/retail-prices-of-commodities-in-india?select=Monthly_Non_Food_Retail_Prices.csv)""",True)
    st.dataframe(helper.monthly_price_df.head(1000))

    st.subheader("Diesel Price")
    st.markdown("""You can download the complete data both petrol and diesel from this [link](https://www.kaggle.com/sudhirnl7/fuel-price-in-india)""",True)
    st.dataframe(die.head(1000))

    st.subheader("Petrol Price")
    st.dataframe(pet.head(1000))


    












# st.plotly_chart(helper.oil_inf())
