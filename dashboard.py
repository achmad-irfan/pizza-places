#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import html
from dash import dash_table
from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import Flask


# In[2]:


app = Flask(__name__)


# In[3]:


data_merge = pd.read_csv('data_merge.csv')
data_merge['date']=pd.to_datetime(data_merge['date'])
data_merge['time']=pd.to_datetime(data_merge['time'])
data_merge['bulan']=data_merge['date'].dt.strftime("%Y-%m")
data_merge['hours']=data_merge['time'].dt.strftime("%H")
data_merge['revenue']=data_merge['quantity']*data_merge['price']
data_merge['hours']=pd.to_numeric(data_merge['hours'])


# In[4]:


options_size = data_merge['size'].unique().tolist()
options_type = data_merge['pizza_type_id'].unique().tolist()
options_month= data_merge['bulan'].unique().tolist()
options_hour= data_merge['hours'].unique().tolist()


# In[5]:


def generate_chart(data, x_column, y_column, chart_type):
    if chart_type == 'bar':
        fig = px.bar(data_frame=data, x=x_column, y=y_column,text_auto=True)
        fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    elif chart_type == 'scatter':
        fig = px.scatter(data_frame=data, x=x_column, y=y_column)
    elif chart_type == 'line':
        fig = px.line(data_frame=data, x=x_column, y=y_column)
        fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
    elif chart_type == 'pie':
        fig= px.pie(data_frame=data, values=x_column,names=y_column)
    else:
        raise ValueError("Invalid chart type. Please choose 'bar', 'scatter', or 'line'.")
    fig.update_layout(width=640, height=410, title={'x':0.5},title_font=dict(size=30),
                      xaxis_title=None,xaxis={'categoryorder':'category ascending'})
    return fig


# In[6]:


fig1= generate_chart(data_merge, data_merge['bulan'].unique(),
                     data_merge.groupby('bulan')['order_id'].count().reset_index()['order_id'],'line')
fig2= generate_chart(data_merge, data_merge['hours'].unique(),
                     data_merge.groupby('hours')['order_id'].count().reset_index()['order_id'],'bar')
fig3= generate_chart(data_merge, data_merge['pizza_type_id'].unique(),
                     data_merge.groupby('pizza_type_id')['quantity'].sum().reset_index()['quantity'],'bar')
fig4= generate_chart(data_merge, 
                     data_merge.groupby('size')['revenue'].sum().reset_index()['revenue'],data_merge['size'].unique(),'pie')
fig5= generate_chart(data_merge, data_merge['pizza_type_id'].unique(),
                     data_merge.groupby('pizza_type_id')['revenue'].sum().reset_index()['revenue'],'bar')
fig6= generate_chart(data_merge, data_merge['bulan'].unique(),
                     data_merge.groupby('bulan')['revenue'].sum().reset_index()['revenue'],'bar')


# In[7]:


title= html.Div([html.H1('PIZZA PLACES DASHBOARD',
                style={'background-color': 'Gainsboro','outline':'10px solid black','font-size':'68px','text-align':'center'})])


# In[8]:


radioitem= dcc.RadioItems(['Size','Month','Hour','Type'],'Size', id='radiobutton',
                          style={'font-size':'30px', 'margin-bottom':'40px', 
                                 'input': {'width': '100px', 'height': '100px','margin-bottom':'10px'}})


# In[9]:


dropdown= dcc.Dropdown([{'label':name ,'value': name} for name in options_size],value=None,id='iddropdown',multi=True, 
                       placeholder='Please Choose',
                       style={'height':'50px','fontSize': '24px'})


# In[10]:


graph = html.Div(children=[
    html.Div([
        html.Div([
            dcc.Graph(id='example-graph1', figure=fig1),
            dcc.Graph(id='example-graph2', figure=fig2)
        ]),
        html.Div([
            dcc.Graph(id='example-graph3', figure=fig3),
            dcc.Graph(id='example-graph4', figure=fig4)
        ]),
        html.Div([
            dcc.Graph(id='example-graph5', figure=fig5),
            dcc.Graph(id='example-graph6', figure=fig6)
        ]),
    ], style={'display': 'flex'})
],style={'float': 'right','width': '85%','outline': '4px solid black','padding': '10px','background':'Gainsboro'})


# In[11]:


menu = html.Div(
    children=[
        html.H2('FILTERS', style={'font-size':'42px','text-align':'center'}),
        radioitem,
        dropdown,
        html.H1(''),
        html.H1(''),
        html.H1(''),
        html.H1(''),
      html.H1(''), html.H1(''), html.H1(''), html.H1(''), html.H1(''), html.H1(''), html.H1('')],
    style={'float': 'left','width': '12.5%','padding': '10px','outline': '4px solid black','backgroundColor':'Gainsboro'})


# In[12]:


app.layout = dbc.Container(
    children=[
        title,
        html.Div(
            children=[
                menu, 
                graph
            ],
            style={'backgroundColor': 'black'}
        )
    ],
    style={'backgroundColor': 'black'}
)


# In[ ]:





# In[13]:


@app.callback(
    Output('iddropdown', 'options'),
    Input('radiobutton','value')
)

def ubah_dropdown(data_filter):
    if data_filter=='Month':
        return [{'label':name,'value':name} for name in options_month]
    if data_filter=='Size':
        return [{'label':name,'value':name} for name in options_size]
    if data_filter=='Hour':
        return [{'label':name,'value':name} for name in options_hour]
    if data_filter== 'Type':
        return [{'label':name,'value':name} for name in options_type]


# In[14]:


@app.callback(
    Output('example-graph1', 'figure'),
    Output('example-graph2', 'figure'),
    Output('example-graph3', 'figure'),
    Output('example-graph4', 'figure'),
    Output('example-graph5', 'figure'),
    Output('example-graph6', 'figure'),
    Input('radiobutton','value'),
    Input('iddropdown','value')
)
    
def filter_input(data_filter,input_filters):
    filtered_data= data_merge.copy()
    input_filters=input_filters or []
    
    if data_filter=='Month' and input_filters is not None:
        filtered_data = filtered_data[filtered_data['bulan'].isin(input_filters)]
    if data_filter=='Size'and input_filters is not None:
        filtered_data = filtered_data[filtered_data['size'].isin(input_filters)]
    if data_filter =='Hour'and input_filters is not None:
        filtered_data = filtered_data[filtered_data['hours'].isin(input_filters)]
    if data_filter == 'Type'and input_filters is not None:
         filtered_data = filtered_data[filtered_data['pizza_type_id'].isin(input_filters)]
        
    fig1 = generate_chart(filtered_data, filtered_data['bulan'].unique(),
                          filtered_data.groupby('bulan')['order_id'].count().reset_index()['order_id'], 'line')
    fig1.update_layout(title={'text': "Total Orders per Month"})
    fig2 = generate_chart(filtered_data, filtered_data['hours'].unique(),
                          filtered_data.groupby('hours')['order_id'].count().reset_index()['order_id'], 'bar')
    fig2.update_layout(title={'text': "Total Orders per Hour"})
    fig3 = generate_chart(filtered_data, filtered_data['pizza_type_id'].unique(),
                          filtered_data.groupby('pizza_type_id')['quantity'].sum().reset_index()['quantity'], 'bar')
    fig3.update_layout(title={'text': "Ranking Most of Popular Pizzas"})
    
    fig4 = generate_chart(filtered_data,
                          filtered_data.groupby('size')['revenue'].sum().reset_index()['revenue'], filtered_data['size'].unique(), 'pie')
    fig4.update_layout(title={'text': "Revenue Contribution by Pizza Sizes"})
    
    fig5 = generate_chart(filtered_data, filtered_data['pizza_type_id'].unique(),
                          filtered_data.groupby('pizza_type_id')['revenue'].sum().reset_index()['revenue'], 'bar')
    fig5.update_layout(title={'text': "Revenue Contribution by Pizza Types"})
    
    fig6 = generate_chart(filtered_data, filtered_data['bulan'].unique(),
                          filtered_data.groupby('bulan')['revenue'].sum().reset_index()['revenue'], 'bar')
    fig6.update_layout(title={'text': "Revenue Contribution by Pizza Types"})
    
    return fig1, fig2, fig3, fig4, fig5, fig6


# In[ ]:


if __name__ == '__main__':
    app.server.run(debug=False, threaded=True)
