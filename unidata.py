# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 21:40:27 2018

@author: ebube
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



#adding data
unidata = pd.read_csv('unidata.csv')
unidata.head(3)
unidata.info()

unidata.student_staff_ratio.value_counts(dropna=False)
#in student_staff_ratio column we have 56 NaN values, lets change them
unidata.student_staff_ratio.mean()
#lets change NaN values with mean of the column which is 18.4
unidata.student_staff_ratio[np.isnan(unidata.student_staff_ratio)] = 18.4
unidata.student_staff_ratio.value_counts(dropna=False)

#type of the student_staff_ratio is object lets change to float
unidata.student_staff_ratio=unidata.student_staff_ratio.astype(float)
unidata.info() # changed

country_list=list(unidata['country'].unique())
#####################################################################
### COUNTRY RANKS ACCORDING TO TEACHING
""" TEACHING RATES OF COUNTRIES """
country_teaching=[]
for i in country_list:
    x = unidata[unidata['country']==i]
    teaching_rate=sum(x.teaching)/len(x)
    country_teaching.append(teaching_rate)
countryranks=pd.DataFrame({'country_list':country_list,'teaching_rate':country_teaching})

increasing_index=(countryranks['teaching_rate'].sort_values(ascending=False)).index.values
sorted_countryranks=countryranks.reindex(increasing_index)
#time to visualization
plt.figure(figsize=(20,15))
ax=sns.barplot(x=sorted_countryranks['country_list'],y=sorted_countryranks['teaching_rate'])
plt.xticks(rotation=270)
plt.xlabel=('Countries')
plt.ylabel=('Rate of teaching')
plt.title('TEACHING RATES OF COUNTRIES')

unidata.info()
#####################################################################
### LETS FIND THE BEST UNIVERSITIES OF FIRST 20 COUNTRIES ACCORDING TO TOTAL_SCORE AND COMPARE THEM
"""TOP 20 COUNTRIES BEST UNI. WHICH HAS MOST TOTAL SCORE"""
unidata.total_score.value_counts()
#i need to fix in data ('-') character first lets make it zero 


unidata.total_score.replace(['-'],0.0,inplace=True)
unidata.total_score.value_counts(dropna=False)
unidata.total_score=unidata.total_score.astype(float)

country_list = list(unidata['country'].unique())
country_ = []
for i in country_list:
    xx = unidata[unidata['country']==i]
    max_total_score = max(xx.total_score)
    country_.append(max_total_score)
country_score=pd.DataFrame({'country':country_list,'max_total_score':country_})
top20=country_score.head(20)

plt.figure(figsize=(15,15))
ax=sns.barplot(x=top20['max_total_score'],y=top20['country'])
plt.xticks(rotation=90)
plt.xlabel("TOP 20 COUNTRIES")
plt.ylabel('MAX TOTAL SCORE OF EACH COUNTRY')
plt.title('TOP 20 COUNTRIES BEST UNI. WHICH HAS MOST TOTAL SCORE')


#####################################################################
### LETS FIND COUNTRIES WHICH HAVE MOST INCOME OF UNIVERSITIES
unidata.income.value_counts(dropna=False)
unidata.income.replace(['-'],0.0,inplace=True)
unidata.income=unidata.income.astype(float)
#I changed characters which we dont want and make them 0 for transform datatype to float from str(object)

country_income=[]
for i in country_list:
    xxx=unidata[unidata['country']==i]
    mean_income=sum(xxx.income)/len(xxx)
    country_income.append(mean_income)
countryincome=pd.DataFrame({'country':country_list,'income':country_income})
top10income=countryincome.head(10)
#while we visualization we would like to see from the highest to lowest income
inc_index=(top10income['income'].sort_values(ascending=False)).index.values
sorted_top10income=top10income.reindex(inc_index)
#lets visualization
plt.figure(figsize=(15,10))
ax=sns.barplot(x=sorted_top10income['country'],y=sorted_top10income['income'])
plt.xticks(rotation=45)
plt.xlabel('TOP COUNTRIES WHICH HAVE HIGHEST INCOME')
plt.ylabel('INCOME')
plt.title(' TOP 10 COUNTRIES WHICH HAVE MOST HIGHER INCOME OF UNIVERSITIES ')


#%% Country Teaching Rate vs Total Score
sorted_countryranks2=sorted_countryranks.copy()
sorted_countryranks2['teaching_rate']=sorted_countryranks2['teaching_rate']/max(sorted_countryranks2['teaching_rate'])
sorted_countryranks2=sorted_countryranks2.head(20)
top20_2=top20
top20_2['max_total_score']=top20_2['max_total_score']/max(top20_2['max_total_score'])
teaching_score=pd.concat([sorted_countryranks2,top20_2['max_total_score']],axis=1)
teaching_score=teaching_score.head(7)
#visiualization
f,ax1=plt.subplots(figsize=(20,10))
sns.pointplot(x='country_list',y='teaching_rate',data=teaching_score,color='lime',alpha=0.8)
sns.pointplot(x='country_list',y='max_total_score',data=teaching_score,color='red',alpha=0.8)
plt.text(40,0.6,'teaching rate',color='lime',fontsize=17,style='italic')
plt.text(40,0.6,'max total score',color='red',fontsize=19,style='italic')
plt.xlabel('Countries',fontsize=15,color='blue')
plt.ylabel('Values',fontsize=15,color='blue')
plt.title('Teaching Rate VS Max Total Score',fontsize=25,color='blue')
plt.grid()
plt.show()


#Show the joint distribution using kernel density estimation
# max_total_score --- teaching_rate 
g = sns.jointplot(teaching_score.teaching_rate,teaching_score.max_total_score, kind="kde", size=7)
plt.savefig('graph.png')
plt.show()











