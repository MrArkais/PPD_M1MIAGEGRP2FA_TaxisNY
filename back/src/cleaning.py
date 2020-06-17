#!/usr/bin/env python
# coding: utf-8

# In[1]:
from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pyspark.sql.functions as F

# In[2]:



def delete_null_data(df, colonne_label):
    
    new_df=df.where(colonne_label + '!= 0' )
    return new_df


# In[4]:


def convert(df, colonne_label, type_to_convert):
    df = df.withColumn(colonne_label, regexp_replace(colonne_label, ',' ,''))
    changed_type_df = df.withColumn(colonne_label, df[colonne_label].cast(type_to_convert))    
    return changed_type_df
                                      
# In[5]:

def convert_date(df,colonne_label):
    date_df = df.withColumn('TIME_'+colonne_label,F.to_timestamp(colonne_label, "MM/dd/yyyy hh:mm:ss aa"))
    return date_df


# In[6]:
def delete_above(df, colonne_label, seuil):
    
    new_df=df.where(colonne_label +'<'+ seuil )
    return new_df

# In[7]:


def delete_under(df, colonne_label, seuil):
    
    new_df=df.where(colonne_label +'>'+ seuil )
    return new_df


# In[8]:


def delete_between(df, colonne_label, seuil_min, seuil_max):
    df1 = delete_above(df, colonne_label, seuil_max)
    df2 = delete_under(df1, colonne_label, seuil_min)    
    return df2


# In[9]:


def mile_to_km(df):
    km= df.withColumn('trip_distance',F.col('trip_distance') / 0.621371)
    return km


# In[10]:


def to_euros(df, colonne_label):
    euros = df.withColumn(colonne_label, F.col(colonne_label) * 0.92)
    return euros

