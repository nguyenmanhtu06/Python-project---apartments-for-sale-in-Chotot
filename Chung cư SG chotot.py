#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#import data, prefix the string with r (to produce a raw string)
chungcu = pd.read_csv(r"C:\Users\Acer\Desktop\Python portfolio\chung cu chotot.csv")

#drop unnamed column
chungcu.drop('Unnamed: 0', axis=1,inplace=True)


# In[2]:


#separate area column into area and bedroom and drop the old area column
chungcu[['Total_area','Bedroom']] = chungcu['area'].str.split('-',expand=True)
chungcu.drop('area', axis=1,inplace=True)
chungcu['Total_area_m2'] = (chungcu['Total_area'].str.split(' ',expand=True))[0]
chungcu.drop('Total_area', axis=1,inplace=True)
chungcu['Total_area_m2'] = chungcu['Total_area_m2'].apply(lambda x: float(x))
#get only apartment between 20 and 200m2
chungcu = chungcu[chungcu['Total_area_m2'].between(20, 200)]


# In[3]:


#get only apartment in medium range i.e. excluding apartment below 1 billion and above 10 billion
chungcu = chungcu[chungcu['price_VND'].str.contains("tỷ")]
#change price column format
wholeprice = lambda x:x.split(' ')[0]
chungcu['Price(bilVND)'] = chungcu['price_VND'].apply(wholeprice)
chungcu['Price(bilVND)'] = chungcu['Price(bilVND)'].str.replace(',','.')
chungcu['Price(bilVND)'] = chungcu['Price(bilVND)'].apply(lambda x: float(x))
chungcu.drop('price_VND',axis=1,inplace=True)
chungcu.drop(chungcu[chungcu['Price(bilVND)'] > 10].index, inplace=True)


# In[4]:


#change quận 9 and Thủ Đức instances to Thủ Đức
#You can perform this task by forming a |-separated string. This works because pd.Series.str.replace accepts regex
thuduc = '|'.join(['Quận 9 - Thành phố Thủ Đức', 'Quận 9', 'Quận Thủ Đức','Quận Thủ Đức - Thành phố Thủ Đức','TP Thủ Đức - Thành phố Thủ Đức'])
chungcu['location'] = chungcu['location'].str.replace(thuduc, 'TP Thủ Đức')
chungcu['location'] = chungcu['location'].str.replace('TP Thủ Đức - Thành phố Thủ Đức','TP Thủ Đức')


# In[5]:


#highest and lowest prices
print(chungcu[chungcu['Price(bilVND)'] == chungcu['Price(bilVND)'].max()])
print(chungcu[chungcu['Price(bilVND)'] == chungcu['Price(bilVND)'].min()])
#average price of the whole city
print(chungcu['Price(bilVND)'].mean())
print(chungcu['Price(bilVND)'].median())
#average price by district
print(chungcu['Price(bilVND)'].groupby(chungcu['location']).mean())

#avg area by district
print(chungcu['Total_area_m2'].groupby(chungcu['location']).mean())
#most common type of apartment
chungcu['Bedroom'].value_counts()

#district with the most and least apartments
chungcu['location'].value_counts()


# In[9]:


#bar chart of prices by district
sns.set_style("dark")
ax1 = sns.barplot(x='Price(bilVND)',y='location',data=chungcu,color='#347deb')
sns.despine()
ax1.set(ylabel=None)


# In[8]:


#scatter plot of prices and areas
sns.scatterplot(data=chungcu,x='Price(bilVND)',y='Total_area_m2')


# In[ ]:




