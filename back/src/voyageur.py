#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark import SparkConf, SparkContext
from pyspark.sql import *
import nbimporter


# In[2]:


from pyspark.sql.types import *
from pyspark.sql import functions as F


# In[3]:


import cleaning as clean


# In[ ]:


# VendorID, zone, total_amount, trip_distance
def get_datas_profile_voyageur(df):
    datas = df.select(['total_amount','trip_distance', 'vendorid','pulocationid','dolocationid']) 
    return datas
       


# In[ ]:


def convert(df):
    
    df_c1 = clean.convert(df, 'total_amount', DoubleType())
    df_c2 = clean.convert(df_c1, 'vendorid', IntegerType())
    df_c3 = clean.convert(df_c2, 'trip_distance', DoubleType())
    
    return df_c3
    


# In[ ]:


def get_zone(df_taxis, df_zones):
    
    df_taxis = df_taxis.join(df_zones, df_zones['locationid'] == df_taxis['pulocationid'],how='inner')
    df_taxis = df_taxis.select(['total_amount','trip_distance', 'vendorid','dolocationid','borough'])
    df_taxis = df_taxis.withColumnRenamed("borough","zone_depart")
    
    df_taxis = df_taxis.join(df_zones, df_zones['locationid'] == df_taxis['dolocationid'],how='inner')
    df_taxis = df_taxis.select(['total_amount','trip_distance', 'vendorid','zone_depart', 'borough'])
    df_taxis = df_taxis.withColumnRenamed("borough","zone_arrivee")

    
    return df_taxis


# In[2]:





# In[ ]:




