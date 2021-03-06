#IMPORTING LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.naive_bayes import BernoulliNB


#IMPORTING DATASET

data=pd.read_csv("corona1.csv",engine="python")
num=len(data)




#LABELS VS VERIFIED AND NON-VERIFIED
   
Y=data.iloc[:,18].values
X=data.iloc[:,11].values
labels=['sad','happy','angry','informative']
v=[0,0,0,0]
n=[0,0,0,0]
for i in range(num):
    if(X[i]==1):
        if(Y[i]=='sad'):
            v[0]=v[0]+1
        elif(Y[i]=='happy'):
            v[1]=v[1]+1
        elif(Y[i]=='angry'):
            v[2]=v[2]+1
        else:
            v[3]=v[3]+1
    else:
        if(Y[i]=='sad'):
            n[0]=n[0]+1
        elif(Y[i]=='happy'):
            n[1]=n[1]+1
        elif(Y[i]=='angry'):
            n[2]=n[2]+1
        else:
            n[3]=n[3]+1
            
#Labels for verified accounts
            
fig,ax=plt.subplots()
ax.bar(labels[0],v[0],color="#000000")
ax.bar(labels[1],v[1],color="#0000CD")
ax.bar(labels[2],v[2],color="#00FFFF")
ax.bar(labels[3],v[3],color="#ADD8E6")     
ax.legend(labels=['sad','happy','angry','informative']) 
plt.xlabel('Emotions')
plt.ylabel('No. of accounts')   
plt.title('Emotions of Verified Users')   
plt.show()
fig.savefig("../flask/static/images/labelsvsverified.png",dpi=100, bbox_inches='tight', pad_inches=0.0)

#Labels for non-verified accounts

fig,ax=plt.subplots()
ax.bar(labels[0],n[0],color="#000000")
ax.bar(labels[1],n[1],color="#0000CD")
ax.bar(labels[2],n[2],color="#00FFFF")
ax.bar(labels[3],n[3],color="#ADD8E6")     
ax.legend(labels=['sad','happy','angry','informative']) 
plt.xlabel('Emotions')
plt.ylabel('No. of accounts')   
plt.title('Emotions of Non-Verified Users')    
plt.show()
fig.savefig("../flask/static/images/labelsvsnv.png",dpi=100, bbox_inches='tight', pad_inches=0.0)


#LABELS VS SENTIMENTS

W=data.iloc[:,18].values

#Encoding data

labelencoder_X = LabelEncoder()
W=labelencoder_X.fit_transform(W)
data['new']=W
Z=data.iloc[:100,[16,19]].values

#Elbow method
'''
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(Z)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
'''

# K Means for sentiment score vs labels
kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(Z)
plt.scatter(Z[y_kmeans == 0, 0], Z[y_kmeans == 0, 1],marker='*',s = 100, c = 'red', label = 'Angry')
plt.scatter(Z[y_kmeans == 1, 0], Z[y_kmeans == 1, 1],marker='P', s = 70, c = 'blue', label = 'Sad')
plt.scatter(Z[y_kmeans == 2, 0], Z[y_kmeans == 2, 1],marker='8', s = 30, c = 'green', label = 'Informative')
plt.scatter(Z[y_kmeans == 3, 0], Z[y_kmeans == 3, 1],marker='2', s = 500, c = 'black',label = 'Happy' )
#plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 30, c = 'yellow', label = 'Centroids')
plt.title('Sentiments VS Emotions')
plt.ylabel('Emotion')
plt.xlabel('Sentiment score')
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
legend_x = 1.5
legend_y = 0.5
plt.legend(loc="center right",bbox_to_anchor=(legend_x, legend_y))
plt.savefig("../flask/static/images/sentivsemo.png",dpi=100, bbox_inches='tight', pad_inches=0.0)

#ANALYSIS OF LABELS

#Label-SAD

Y=data.iloc[:,18].values
X=data.iloc[:,11].values
labels=['sad','happy','angry','informative']
Z=[]
for i in labels:
    c=0
    for j in range(num):
        if(Y[j]==i):
            c=c+1
    Z.append(c)
svno=[0,0]   
for i in range(num):
    if(Y[i]=='sad'):
        if(X[i]==1):
           svno[0]=svno[0]+1
        else:
            svno[1]=svno[1]+1
            
#Pie Chart for Sad
            
labels = 'Verified','Non-Verified'
sizes=svno
explode = (0.1, 0)  
colors=['#A74AC7','#461B7E']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels,colors=colors, autopct='%1.1f%%',shadow=True, startangle=180)
ax1.axis('equal') 
plt.title('Sad comments')
fig1.savefig("../flask/static/images/Sad.png")

#Label-HAPPY

hvno=[0,0]   
for i in range(num):
    if(Y[i]=='happy'):
        if(X[i]==1):
            hvno[0]=hvno[0]+1
        else:
            hvno[1]=hvno[1]+1
            
#Pie Chart for Happy
            
labels = 'Verified','Non-Verified'
sizes=hvno
explode = (0.1, 0)  
colors=['#FFDB58','#8B4513']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode,colors=colors, labels=labels, autopct='%1.1f%%',shadow=True, startangle=180)
ax1.axis('equal') 
plt.title('Happy comments') 
plt.show()
fig1.savefig("../flask/static/images/Happy.png")

#Label-ANGRY

avno=[0,0]   
for i in range(num):
    if(Y[i]=='angry'):
        if(X[i]==1):
            avno[0]=avno[0]+1
        else:
            avno[1]=avno[1]+1
            
#Pie Chart for Angry
            
labels = 'Verified','Non-Verified'
sizes=avno
colors=['#F75D59','#CC0000']
explode = (0.1, 0)  

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels,colors=colors, autopct='%1.1f%%',shadow=True, startangle=180)
ax1.axis('equal') 
plt.title('Angry comments')
plt.show()
fig1.savefig("../flask/static/images/Angry.png")

#Label-INFORMATIVE

ivno=[0,0]   
for i in range(num):
    if(Y[i]=='informative'):
        if(X[i]==1):
            ivno[0]=avno[0]+1
        else:
            ivno[1]=avno[1]+1
            
#Pie Chart for Informative
            
labels = 'Verified','Non-Verified'
sizes=ivno
colors=['#FFB6C1','#FF1493']
explode = (0.1, 0)  
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode,colors=colors, labels=labels, autopct='%1.1f%%',shadow=True, startangle=180)
ax1.axis('equal') 
plt.title('Informative comments') 
plt.show()
fig1.savefig("../flask/static/images/Informative.png")

#OVERALL CHART FOR LABELS

#Pie Chart for Labels

labels = 'Angry','Happy','Sad','Informative'
sizes=Z
explode = (0, 0.1,0,0)  
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True,startangle=180)
ax1.axis('equal') 
plt.title('Tweet emotions') 
plt.show()
fig1.savefig("../flask/static/images/Labels.png")

#Donut Chart

labels =['Angry','Happy','Sad','Informative']
sizes=Z
colors = ['#EC83D9','#A74AC7','#461B7E','#ED1FC4']
my_circle=plt.Circle( (0,0), 0.5, color='white')
patches, texts=plt.pie(sizes,colors=colors)
plt.rcParams['text.color'] = 'black'
plt.legend(patches, labels, loc=1)
plt.title('Tweet Emotions')
p=plt.gcf()
plt.pie(sizes,colors=colors, wedgeprops = { 'linewidth':2, 'edgecolor' : 'white' },autopct='%1.1f%%',pctdistance=0.7)
p.gca().add_artist(my_circle)
p.savefig("../flask/static/images/Labels1.png")
plt.show()
