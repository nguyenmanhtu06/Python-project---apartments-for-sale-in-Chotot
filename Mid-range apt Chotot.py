#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[15]:


#import data, prefix the string with r (to produce a raw string)
chungcu = pd.read_csv(r"C:\Users\Acer\Desktop\Python pj 1\chung cu chotot.csv")

#drop unnamed column
chungcu.drop('Unnamed: 0', axis=1,inplace=True)


# In[16]:


#separate area column into area and bedroom and drop the old area column

chungcu[['Total_area','Bedroom']] = chungcu['area'].str.split('-',expand=True)
chungcu.drop('area', axis=1,inplace=True)
chungcu['Total_area_m2'] = (chungcu['Total_area'].str.split(' ',expand=True))[0]
chungcu.drop('Total_area', axis=1,inplace=True)
chungcu['Total_area_m2'] = chungcu['Total_area_m2'].apply(lambda x: float(x))

#get only apartment between 20 and 120m2

chungcu = chungcu[chungcu['Total_area_m2'].between(20, 120)]


# In[17]:


#get only apartment in medium range i.e. excluding apartment below 1 billion and above 10 billion

chungcu = chungcu[chungcu['price_VND'].str.contains("tỷ")]

#split the column to get numbers only, then change data type from object to float

wholeprice = lambda x:x.split(' ')[0]
chungcu['Price(bilVND)'] = chungcu['price_VND'].apply(wholeprice)
chungcu['Price(bilVND)'] = chungcu['Price(bilVND)'].str.replace(',','.')
chungcu['Price(bilVND)'] = chungcu['Price(bilVND)'].apply(lambda x: float(x))

chungcu.drop('price_VND',axis=1,inplace=True)

#excluding apartments above 10bn VND
chungcu.drop(chungcu[chungcu['Price(bilVND)'] > 10].index, inplace=True)
chungcu


# In[18]:


#change quận 9 and Thủ Đức instances to Thủ Đức. You can perform this task by forming a |-separated string. This works because pd.Series.str.replace accepts regex

thuduc = '|'.join(['Quận 9 - Thành phố Thủ Đức', 'Quận 9', 'Quận Thủ Đức','Quận Thủ Đức - Thành phố Thủ Đức','TP Thủ Đức - Thành phố Thủ Đức'])
chungcu['location'] = chungcu['location'].str.replace(thuduc, 'TP Thủ Đức')
chungcu['location'] = chungcu['location'].str.replace('TP Thủ Đức - Thành phố Thủ Đức','TP Thủ Đức')


# In[33]:


#highest and lowest prices

print(chungcu[chungcu['Price(bilVND)'] == chungcu['Price(bilVND)'].max()])
print(chungcu[chungcu['Price(bilVND)'] == chungcu['Price(bilVND)'].min()])

#average price and median price of the whole city

print(chungcu['Price(bilVND)'].mean())
print(chungcu['Price(bilVND)'].median())

#average price by district

print(chungcu['Price(bilVND)'].groupby(chungcu['location']).mean().sort_values(ascending=False))


# In[34]:


#avg area by district

print(chungcu['Total_area_m2'].groupby(chungcu['location']).mean())

#most common type of apartment

chungcu['Bedroom'].value_counts()

#district with the most and least apartments

chungcu['location'].value_counts()


# In[29]:


#bar chart of prices by district

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot()
sns.set_style("dark")
ax1 = sns.barplot(x='Price(bilVND)',y='location',data=chungcu,color='#347deb')
sns.despine()
ax1.set(ylabel=None)


# In[35]:


#scatter plot of prices and areas

fig2 = plt.figure(figsize=(12,8))
ax2 = fig2.add_subplot()
sns.scatterplot(data=chungcu,x='Total_area_m2',y='Price(bilVND)')


# In[ ]:




