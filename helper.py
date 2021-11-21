from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio




monthly_price_df = pd.read_csv('monthly_price.csv')

# state = monthly_price_df['state'].unique().to_list()
# commodity = monthly_price_df['commodity'].unique().to_list()
"""
---------------------------------------------------------------------------------------------------------------------------------------
# Commodity Price Over Years
---------------------------------------------------------------------------------------------------------------------------------------
"""


def price_comm(state,commodity):
    cent = monthly_price_df[monthly_price_df['state'] == state].groupby(['year','commodity']).mean()
    cent = pd.DataFrame(cent)
    cent = cent.reset_index()
    
    comm = cent[cent['commodity'] == commodity]
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x= comm['year'],
        y= comm['retail_price(in Rs.)'],
        opacity = 0.6,
        # hovertemplate="%{y}%{_xother}",
        marker_color = 'purple'
    ))

    fig.add_trace(go.Scatter(
        x= comm['year'],
        y= comm['retail_price(in Rs.)'],
        line = dict(shape = 'linear', color = 'rgb(205, 12, 24)', width= 3, dash = 'dot'),
        mode = "lines+markers",
        marker = dict(symbol = "circle", color = 'rgb(205, 12, 24)',size = 6),
        connectgaps = True,
        # hovertemplate="%{y}%{_xother}"
    ))

    fig.update_layout(plot_bgcolor = "white",hovermode="x unified",
        title={
        'text': "Price over Years",
        'y':0.9,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Year",
        yaxis_title="Price (in Rs)",
        legend_title="Legend Title",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="RebeccaPurple"
    ))

    return fig
    # fig.show()

# price_comm('Jharkhand','Mustard Oil')




"""
---------------------------------------------------------------------------------------------------------------------------------------
# Inflation over years
---------------------------------------------------------------------------------------------------------------------------------------
"""

def inflation(state,commodity):
    cent = monthly_price_df[monthly_price_df['state'] == state].groupby(['year','commodity']).mean()
    cent = pd.DataFrame(cent)
    cent = cent.reset_index()
    
    comm = cent[cent['commodity'] == commodity].copy()
    price_arr = comm['retail_price(in Rs.)'].shift(periods =1)
    comm['inflation(in %)'] = ((comm['retail_price(in Rs.)'] - price_arr)/comm['retail_price(in Rs.)']) *100
    
    fig1 = px.bar(comm, x='year', y='inflation(in %)')
    fig1.update_layout(plot_bgcolor = "white",hovermode="x unified",
        title={
        'text': "Inflation(%) over Years",
        'y':0.9,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Year",
        yaxis_title="Inflation(in %)",
        legend_title="Legend Title",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="RebeccaPurple"
    ))
    # fig.show()
    
    return fig1
    # fig.show()

def inf_df(state,commodity):
    cent = monthly_price_df[monthly_price_df['state'] == state].groupby(['year','commodity']).mean()
    cent = pd.DataFrame(cent)
    cent = cent.reset_index()
    
    comm = cent[cent['commodity'] == commodity].copy()
    price_arr = comm['retail_price(in Rs.)'].shift(periods =1)
    comm['inflation(in %)'] = ((comm['retail_price(in Rs.)'] - price_arr)/comm['retail_price(in Rs.)']) *100

    df = comm.reset_index()
    df = df.loc[:,['year','retail_price(in Rs.)','inflation(in %)']]
    df = df.round(2)
    fig = ff.create_table(df,index=False)
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 20

    return fig




# inflation('Jharkhand','Mustard Oil')


"""
---------------------------------------------------------------------------------------------------------------------------------------
# Diesel & Petrol vs Commodity
---------------------------------------------------------------------------------------------------------------------------------------
"""


diesel_df = pd.read_csv('diesel.csv')
petrol_df = pd.read_csv('petrol.csv')
diesel_df['date'] = pd.to_datetime(diesel_df['date'])
diesel_df['year'] = diesel_df['date'].dt.year

petrol_df['date'] = pd.to_datetime(petrol_df['date'])
petrol_df['year'] = petrol_df['date'].dt.year

pet_df = petrol_df.iloc[:,2:]
die_df = diesel_df.iloc[:,2:]
pet_df = pet_df.groupby('year').mean()
die_df = die_df.groupby('year').mean()
pet_df.columns = ['petrol(in Rs.)']
die_df.columns = ['diesel(in Rs.)']



def fuel_economy(state,commodity):
    cent = monthly_price_df.groupby(['year','commodity']).mean()
    cent = pd.DataFrame(cent)
    cent = cent.reset_index()
    
    comm = cent[cent['commodity'] == commodity].copy()
    
#     comm = comm.iloc[1:-1]
    comm.set_index('year',inplace = True)
    combine = pd.concat([comm,pet_df,die_df],axis = 1)
    combine.reset_index(inplace = True)

    crr = combine['retail_price(in Rs.)'].corr(combine['petrol(in Rs.)'])
    
    
    fig = px.scatter(combine, y="retail_price(in Rs.)", x="petrol(in Rs.)",color = 'year',
                     hover_data=['year'])
    fig.update_traces(marker_size=10)
    return [fig,crr]

def fuel_economy2(state,commodity):
    cent = monthly_price_df.groupby(['year','commodity']).mean()
    cent = pd.DataFrame(cent)
    cent = cent.reset_index()
    
    comm = cent[cent['commodity'] == commodity].copy()
    
#     comm = comm.iloc[1:-1]
    comm.set_index('year',inplace = True)
    combine = pd.concat([comm,pet_df,die_df],axis = 1)
    combine.reset_index(inplace = True)

    crr = combine['retail_price(in Rs.)'].corr(combine['diesel(in Rs.)'])

    fig = px.scatter(combine, y="retail_price(in Rs.)", x="diesel(in Rs.)",color = 'year',
                     hover_data=['year'])
    fig.update_traces(marker_size=10)
    return [fig,crr]



    
# print("The Correlation b/w Petrol and Commodity Price is ",combine['retail_price(in Rs.)'].corr(combine['petrol(in Rs.)']))
# print("The Correlation b/w Diesel and Commodity Price is ",combine['retail_price(in Rs.)'].corr(combine['diesel(in Rs.)']))

# fuel_economy('Maharashtra','Mustard Oil')





"""
---------------------------------------------------------------------------------------------------------------------------------------
# Price at different States
---------------------------------------------------------------------------------------------------------------------------------------
"""  

def state_wise_price(commodity,year):
    cent = monthly_price_df[monthly_price_df['commodity'] == commodity]
    cent = cent.groupby(['state','year']).mean()
    cent = pd.DataFrame(cent)
    cent.reset_index(inplace = True)
    cent = cent.iloc[:,:3]
    cent = cent[cent['year'] == year]
    cent['state'].replace({'Jammu Kashmir' : 'Jammu & Kashmir',
                            'Orissa' : 'Odisha',
                             'National Capital' : 'Delhi'},inplace = True)
    
    a = {'state':'Chhattisgarh', 'year':year,'retail_price(in Rs.)':0}
    b = {'state':'Ladakh', 'year':year,'retail_price(in Rs.)':0}
    cent = cent.append(a, ignore_index = True)
    cent = cent.append(b,ignore_index = True)
    cent['retail_price(in Rs.)'] = cent['retail_price(in Rs.)'].fillna(0)
    
    
    fig = px.choropleth(
    cent,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color='retail_price(in Rs.)',
    labels={'retail_price(in Rs.)':'retail_price(in Rs.)'},
     color_continuous_scale='Viridis',
   )

    fig.update_geos(fitbounds="locations", visible=False)

    # fig.show()
    
    

    return fig

def state_wise(commodity,year):

    cent = monthly_price_df[monthly_price_df['commodity'] == commodity]
    cent = cent.groupby(['state','year']).mean()
    cent = pd.DataFrame(cent)
    cent.reset_index(inplace = True)
    cent = cent.iloc[:,:3]
    cent = cent[cent['year'] == year]
    cent['state'].replace({'Jammu Kashmir' : 'Jammu & Kashmir',
                            'Orissa' : 'Odisha',
                             'National Capital' : 'Delhi'},inplace = True)
    
    a = {'state':'Chhattisgarh', 'year':year,'retail_price(in Rs.)':0}
    b = {'state':'Ladakh', 'year':year,'retail_price(in Rs.)':0}
    cent = cent.append(a, ignore_index = True)
    cent = cent.append(b,ignore_index = True)
    cent['retail_price(in Rs.)'] = cent['retail_price(in Rs.)'].fillna(0)



    df = cent
    df = df.round(2)
    fig2 = ff.create_table(df,index=False)
    for i in range(len(fig2.layout.annotations)):
        fig2.layout.annotations[i].font.size = 20

    return fig2

# state_wise_price('Moong',2021)



"""
---------------------------------------------------------------------------------------------------------------------------------------
# State vs State comparison¶
---------------------------------------------------------------------------------------------------------------------------------------
"""  


def state_comp(commodity,year,state):
    cent = monthly_price_df[monthly_price_df['commodity'] == commodity]
    cent = cent.groupby(['state','year']).mean()
    cent = pd.DataFrame(cent)
    cent.reset_index(inplace = True)
    cent = cent.iloc[:,:3]
    cent = cent[cent['retail_price(in Rs.)'].notnull()]
    cent = cent[cent['year'] == year]
    a = cent['retail_price(in Rs.)'].idxmax()
    b = cent['retail_price(in Rs.)'].idxmin()
    c = cent.index[cent['state'] == state].tolist()[0]
    my_list = [a,b,c]
#     reqd_df = cent.iloc[[a,b,c]]
    Filter_df  = cent[cent.index.isin(my_list)]
    
    fig = go.Figure(go.Bar(
            y= Filter_df['state'],
            x= Filter_df['retail_price(in Rs.)'],
            orientation='h',
            marker=dict(
        color='rgba(164, 163, 204, 0.85)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=0.5),
            )))
    fig.update_layout(plot_bgcolor = "white",hovermode="x unified",
        title={
        'text': "Given State vs Min and Max State",
        'y':0.9,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Retail Price(in Rs.)",
        yaxis_title="Sate",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="RebeccaPurple"
    ))

    # fig.show()
    
    
    fig2 = ff.create_table(Filter_df,index=False)
    for i in range(len(fig2.layout.annotations)):
        fig2.layout.annotations[i].font.size = 20

    # fig.show()

    return fig

def state_comp_df(commodity,year,state):
    cent = monthly_price_df[monthly_price_df['commodity'] == commodity]
    cent = cent.groupby(['state','year']).mean()
    cent = pd.DataFrame(cent)
    cent.reset_index(inplace = True)
    cent = cent.iloc[:,:3]
    cent = cent[cent['retail_price(in Rs.)'].notnull()]
    cent = cent[cent['year'] == year]
    a = cent['retail_price(in Rs.)'].idxmax()
    b = cent['retail_price(in Rs.)'].idxmin()
    c = cent.index[cent['state'] == state].tolist()[0]
    my_list = [a,b,c]

    Filter_df  = cent[cent.index.isin(my_list)]
    fig2 = ff.create_table(Filter_df,index=False)
    for i in range(len(fig2.layout.annotations)):
        fig2.layout.annotations[i].font.size = 20
    
    return fig2




    

# state_comp('Mustard Oil',2021,'Jharkhand')


"""
---------------------------------------------------------------------------------------------------------------------------------------
# OIL Economy
---------------------------------------------------------------------------------------------------------------------------------------
"""
diesel_df['my'] = diesel_df['date'].dt.to_period('M')
die = diesel_df.groupby('my').mean()

petrol_df['my'] = petrol_df['date'].dt.to_period('M')
pet = petrol_df.groupby('my').mean()

merge_df = pd.merge(left = die, right = pet,left_index = True, right_index = True)
merge_df = merge_df.iloc[:,:-1]
merge_df.columns = ['diesel','year','petrol']

    


def oil_economy():
    
    fig = go.Figure()
    merge_df.index = merge_df.index.astype('str')   
    fig.add_trace(go.Scatter(
            x= merge_df.index,
            y= merge_df['diesel'],
            line = dict(shape = 'linear', color = 'rgb(205, 12, 24)', width= 3, dash = 'dot'),
            mode = "lines+markers",
            marker = dict(symbol = "circle", color = 'rgb(205, 12, 24)',size = 2),
            connectgaps = True,
            hovertemplate="%{y}%{_xother}",
            name = 'diesel'
        ))

    fig.add_trace(go.Scatter(
            x= merge_df.index,
            y= merge_df['petrol'],
            line = dict(shape = 'linear', color = 'blue', width= 3, dash = 'dot'),
            mode = "lines+markers",
            marker = dict(symbol = "circle", color = 'blue',size = 2),
            connectgaps = True,
            hovertemplate="%{y}%{_xother}",
            name = 'petrol'
        ))

    fig.update_layout(plot_bgcolor = "white",hovermode="x unified",
            title={
            'text': "Price over Years",
            'y':0.9,
            'x':0.44,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title="Year",
            yaxis_title="Price (in Rs)",
            legend_title="OIL",
            font=dict(
            family="Courier New, monospace",
            size=20,
            color="RebeccaPurple"
        
        ))
        
        
    return fig

# oil_economy()


def oil_inf():
    diesel_df['my'] = diesel_df['date'].dt.to_period('M')
    die = diesel_df.groupby('my').mean()

    petrol_df['my'] = petrol_df['date'].dt.to_period('M')
    pet = petrol_df.groupby('my').mean()

    merge_df = pd.merge(left = die, right = pet,left_index = True, right_index = True)
    merge_df = merge_df.iloc[:,:-1]
    merge_df.columns = ['diesel','year','petrol']

    merge_df.index = merge_df.index.astype('str')  
    merge_df = merge_df.groupby('year').mean()
    price_arr = merge_df['diesel'].shift(periods =1)
    merge_df['diesel_inflation(in %)'] = ((merge_df['diesel'] - price_arr)/merge_df['diesel'] ) *100
    price_arr = merge_df['petrol'].shift(periods =1)
    merge_df['petrol_inflation(in %)'] = ((merge_df['petrol'] - price_arr)/merge_df['petrol'] ) *100
    merge_df = merge_df.iloc[1:]

    #fig = px.bar(merge_df, x=merge_df.index, y='diesel_inflation(in %)')
    fig = go.Figure(data=[
        go.Bar(name='diesel', x=merge_df.index, y= merge_df['diesel_inflation(in %)']),
        go.Bar(name='petrol', x=merge_df.index, y= merge_df['petrol_inflation(in %)'])
    ])
    fig.update_layout(plot_bgcolor = "white",hovermode="x unified",
            title={
            'text': "Inflation(%) over Years",
            'y':0.9,
            'x':0.48,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title="Year",
            yaxis_title="Inflation(in %)",
            legend_title="Legend Title",
            font=dict(
            family="Courier New, monospace",
            size=20,
            color="RebeccaPurple"
        ))

    return fig

    # fig.show()

# oil_inf()


