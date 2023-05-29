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
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc


# In[2]:


app= dash.Dash(__name__)
server=app.server

app.layout = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"),
    className="p-5",
)


# In[3]:


data_merge = pd.read_csv('data_merge.csv')
data_merge['date']=pd.to_datetime(data_merge['date'])
data_merge['time']=pd.to_datetime(data_merge['time'])
data_merge['bulan']=data_merge['date'].dt.strftime("%Y-%m")
data_merge['hours']=data_merge['time'].dt.strftime("%H")
data_merge['revenue']=data_merge['quantity']*data_merge['price']
data_merge['hours']=pd.to_numeric(data_merge['hours'])
filtered_data = data_merge.copy()
selected_size = 'L'
filtered_data = filtered_data[filtered_data['size'] == selected_size]
filtered_data


# In[4]:


options_size = data_merge['size'].unique()
options_type = data_merge['pizza_type_id'].unique()
options_month= data_merge['bulan'].unique()
options_hour= data_merge['hours'].unique()


# In[5]:


data_size = data_merge[data_merge['size'] == 'XXL']
data_size.shape
px.line(data_size, x=data_size['bulan'].unique(), y=data_size.groupby('bulan').count().reset_index()['order_id'])


# In[6]:


def generate_chart(data, x_column, y_column, chart_type):
   if chart_type == 'bar':
       fig = px.bar(data_frame=data, x=x_column, y=y_column)
       fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
   elif chart_type == 'scatter':
       fig = px.scatter(data_frame=data, x=x_column, y=y_column)
   elif chart_type == 'line':
       fig = px.line(data_frame=data, x=x_column, y=y_column)
       fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
   elif chart_type == 'pie':
       fig= px.pie(data_frame=data, values=x_column,names=y_column)
   else:
       raise ValueError("Invalid chart type. Please choose 'bar', 'scatter', or 'line'.")
   fig.update_layout(width=640, height=410, title={'x':0.5},title_font=dict(size=30),xaxis_title=None,xaxis={'categoryorder':'category ascending'})
   return fig


# In[ ]:





# In[7]:


fig1= generate_chart(data_merge, data_merge['bulan'].unique(),
                     data_merge.groupby('bulan')['order_id'].count().reset_index()['order_id'],'line')
fig1.update_layout(
    title={'text': "Total Orders per Month"})


# In[8]:


fig2= generate_chart(data_merge, data_merge['hours'].unique(),
                     data_merge.groupby('hours')['order_id'].count().reset_index()['order_id'],'bar')
fig2.update_layout(
    title={'text': "Total Orders per Hour"})


# In[9]:


fig3= generate_chart(data_merge, data_merge['pizza_type_id'].unique(),
                     data_merge.groupby('pizza_type_id')['quantity'].sum().reset_index()['quantity'],'bar')
fig3.update_layout(
    title={'text': "Ranking Most of Popular Pizzas"})


# In[10]:


fig4= generate_chart(data_merge, 
                     data_merge.groupby('size')['revenue'].sum().reset_index()['revenue'],data_merge['size'].unique(),'pie')
fig4.update_layout(
    title={'text': "Revenue Contribution by Pizza Sizes"})


# In[11]:


fig5= generate_chart(data_merge, data_merge['pizza_type_id'].unique(),
                     data_merge.groupby('pizza_type_id')['revenue'].sum().reset_index()['revenue'],'bar')
fig5.update_layout(
    title={'text': "Revenue Contribution by Pizza Types"})


# In[12]:


fig6= generate_chart(data_merge, data_merge['bulan'].unique(),
                     data_merge.groupby('bulan')['revenue'].sum().reset_index()['revenue'],'bar')
fig6.update_layout(
    title={'text': "Revenue Contribution by Pizza Types"})


# In[ ]:





# In[13]:


title= html.Div([html.H1('PIZZA PLACES DASHBOARD',
                style={'background-color': 'gray','font-size':'68px','text-align':'center'})])


# In[14]:


def dropdown(id,option_item,tipe,nama):
    if tipe== 'item':
        return dcc.Dropdown(
        id=id,
        options=[{'label': nama, 'value': nama} for nama in option_item],
        value=None,style={'height': '50px','margin-bottom': '25px'},placeholder='Please Choose')
    elif tipe=='judul':
        return html.Label(
        str(nama+' :'),
        htmlFor=id,
        style={'text-align':'center','font-size':'32px','margin-bottom': '10px' })


# In[15]:


dropdown_size = dropdown('dropdown-input-size',options_size,'item','size')
dropdown_size_title = dropdown('dropdown-title-size',options_size,'judul','size')


# In[16]:


dropdown_type = dropdown('dropdown-input-type',options_type,'item','type')
dropdown_type_title = dropdown('dropdown-title-type',options_type,'judul','type')


# In[17]:


dropdown_month = dropdown('dropdown-input-month',options_month,'item','month')
dropdown_month_title = dropdown('dropdown-title-month',options_month,'judul','month')


# In[18]:


dropdown_hour = dropdown('dropdown-input-hour',options_hour,'item','hour')
dropdown_hour_title = dropdown('dropdown-title-hour',options_hour,'judul','hour')


# In[19]:


menu = html.Div(
    children=[
        html.H2('FILTERS', style={'font-size':'42px','text-align':'center'}),
        dropdown_month_title,
        dropdown_month,
        dropdown_hour_title,
        dropdown_hour,
        dropdown_size_title,
        dropdown_size,
        dropdown_type_title,
        dropdown_type,
    ],style={'float': 'left','width': '13%','padding': '2px'})


# In[20]:


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
],style={'float': 'right','width': '86%','outline': '5px solid black','padding': '5px'})


# In[21]:


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


# In[22]:


@app.callback(
    Output('example-graph1', 'figure'),
    Output('example-graph2', 'figure'),
    Output('example-graph3', 'figure'),
    Output('example-graph4', 'figure'),
    Output('example-graph5', 'figure'),
    Output('example-graph6', 'figure'),
    Input('dropdown-input-hour', 'value'),
    Input('dropdown-input-size', 'value'),
    Input('dropdown-input-month', 'value'),
    Input('dropdown-input-type', 'value'),
)
def update_graphs(selected_hour,selected_size,selected_month,selected_type):
    filtered_data = data_merge.copy()
    
    if selected_hour is not None:
        filtered_data = filtered_data[filtered_data['hours'] == selected_hour]
    elif selected_size is not None:
        filtered_data = filtered_data[filtered_data['size'] == selected_size]
    elif selected_month is not None:
        filtered_data = filtered_data[filtered_data['bulan'] == selected_month]
    elif selected_type is not None:
        filtered_data = filtered_data[filtered_data['pizza_type_id'] == selected_type]
    
    fig1 = generate_chart(filtered_data, filtered_data['bulan'].unique(),
                          filtered_data.groupby('bulan')['order_id'].count().reset_index()['order_id'], 'line')
    fig1.update_layout(title={'text': "Total Orders per Month"})
    
    fig2 = generate_chart(filtered_data, filtered_data['hours'].unique(),
                          filtered_data.groupby('hours')['order_id'].count().reset_index()['order_id'], 'bar')
    fig2.update_layout(title={'text': "Total Orders per Hour"},text_auto=True)
    
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
    app.run(debug=True)


# In[ ]:





# In[ ]:





# In[ ]:




