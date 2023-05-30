<p align="right"> <a href="https://achmadirfana.github.io/portofolio/portfolio-pizza-place.html">Back</a></p>


<h2>  Pizza Places</h2>
<p> URL Dashoboard project : <a href="https://pizza-places.onrender.com/">Pizza Places</a></p>
<h3> Background Project :</h3>
<p> work as an analyst for the Pizza Place restaurant. My boss asked you to analyze the restaurant's performance in 2015 </p>
<h3>Purpose:</h3>
<p style="margin-left: 20px;text-align:justify">  The main purpose is to provide a number of isnight and recomendation about the data. To do this,
first I  need to identify the following data:</p>
<p style="margin-left: 20px">•  How many orders do we get each month? What month have the highest sales? Display in the form of a line chart. </p>
<p style="margin-left: 20px">•  Are there peak hours? Display in bar plot form. </p>
<p style="margin-left: 20px">•  What's the most ordered pizza? Compare order quantities on each type of pizza with a bar plot  </p>
<p style="margin-left: 20px">•  What is the revenue contribution for each pizza size? Show in the form of a pie chart</p>
<p style="margin-left: 20px">•  How is the revenue contribution for each type of pizza? Display in the form of bar plots, sorted from the highest contribution.</p>
<p style="margin-left: 20px">•  What is the revenue in every month </p>
<h3>Datas:</h3>
<h4>Dataset:</h4>
<p>In this project, it used 3 csv files, orders, order_details, and pizzas, that can be accessed in the following link:</p>
<p><p align="left"> <a href="https://drive.google.com/file/d/1Kfsd39u3bQujcwm6qDGvidlH5Lqc8wiJ/view?usp=share_link">orders</a></p> </p>
<p><p align="left"> <a href="https://drive.google.com/file/d/1arl5qCDzmMLRTK9WMQmDCthgWZELrEQD/view?usp=share_link">order_details</a></p> </p>
<p><p align="left"> <a href="https://drive.google.com/file/d/1FCHb0csgSgaal3sMgVCMu4PS-eb5qYBg/view?usp=share_link">pizzas</a></p> </p>
<p>each file is data from 2015 and must be imported to jupyter notebook</p>


<h3>Data Preparation</h3>
<p> All files must be put in the same folder/directory as python </p>
<h4>Data Validation</h4>
<p style="margin-left: 30px"> All the data must be checked whetever there is a abnormal data. The  queery for data checking and validating :</p>
<div style="margin-left: 30px;height:200px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
  <p style="margin-left: 20px">import pandas as pd </p>
<p style="margin-left: 20px">import seaborn as sns </p>
<p style="margin-left: 20px">import matplotlib.pyplot as plt </p>
<p style="margin-left: 20px">import calendar </p>
<p style="margin-left: 20px">order= pd.read_csv("orders.csv") </p>
<p style="margin-left: 20px">order_detail= pd.read_csv("order_details.csv") </p>
<p style="margin-left: 20px">pizzas= pd.read_csv("pizzas.csv") </p>
<p style="margin-left: 20px">order_detail.isnull().any() #Checking data blank in file order_detail </p>
<p style="margin-left: 20px">pizzas.isnull().any() #Checking data blank in file pizzas </p>
</div> 

<h4>Data Duplicate Checking</h4>
<p style="margin-left: 30px"> Code for data duplicate checking :</p>
<div style="margin-left: 30px;height:50px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
  <p style="margin-left: 20px">order.duplicated('order_id').any() #Checking whetevr any duplicate data in data order column order_id </p>
</div> 
<h3>Dat Analyze</h3>
<h4>1. Total Order per Month</h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:80px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">order['date']=pd.to_datetime(order['date']) </p>
<p style="margin-left: 20px">order['month']=order['date'].dt.strftime("%Y-%m") </p>
<p style="margin-left: 20px">plt.figure(figsize=(11,4)) </p>
<p style="margin-left: 20px">sns.lineplot(data=order.groupby('month')['order_id'].count().reset_index(),x='month',y='order_id') </p>
<p style="margin-left: 20px">plt.title('Total Orders per Month') </p>
<p style="margin-left: 20px">plt.ylabel('Total Transaction') </p>
<p style="margin-left: 20px">plt.xlabel('Month') </p>
<p style="margin-left: 20px">plt.show </p>
</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="no-1.png" class="img-fluid" alt="">  
</p>

<h4>2. Total Order per Hours</h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:80px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">order['time']=pd.to_datetime(order['time']) </p>
<p style="margin-left: 20px">order['hours']=order['time'].dt.strftime("%H") </p>
<p style="margin-left: 20px">order_hour= order.groupby('hours')['order_id'].count().reset_index() </p>
<p style="margin-left: 20px">order_hour.to_csv('order_hour.csv',index=False) </p>
<p style="margin-left: 20px">plt.figure(figsize=(8,4)) </p>
<p style="margin-left: 20px">sns.barplot(data=order_hour, x='hours', y='order_id') </p>
<p style="margin-left: 20px">plt.title('Orders by Hours') </p>
<p style="margin-left: 20px">plt.xlabel('Hours') </p>
<p style="margin-left: 20px">plt.ylabel('Total Transaction') </p>
<p style="margin-left: 20px">plt.show </p>
</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="no-2.png" class="img-fluid" alt="">  
</p>

<h4>3. Ranking Most of Popular Pizzas</h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:80px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">data_merge = pd.merge(order_detail,pizzas,on='pizza_id') </p>
<p style="margin-left: 20px">data_merge_quantity= data_merge.groupby('pizza_type_id')['quantity'].sum().reset_index() </p>
<p style="margin-left: 20px">data_merge_quantity.to_csv('data_merge_quantity.csv',index=False) </p>
<p style="margin-left: 20px">plt.figure(figsize=(11,8)) </p>
<p style="margin-left: 20px">plt.xticks(rotation='vertical') </p>
<p style="margin-left: 20px">sns.barplot(data=data_merge_quantity.sort_values('quantity', ascending=False),x='pizza_type_id',y='quantity') </p>
<p style="margin-left: 20px">plt.title('Ranking Most of Popular Pizzas') </p>
<p style="margin-left: 20px">plt.xlabel('Pizza Type') </p>
<p style="margin-left: 20px">plt.ylabel('Total Orders') </p>
<p style="margin-left: 20px">plt.show </p>
</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="no-3.png" class="img-fluid" alt="">  
</p>
