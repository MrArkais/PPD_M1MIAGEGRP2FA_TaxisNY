#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql import functions as F
import json
from pyspark.sql.utils import AnalysisException
from pyspark.sql import Row


# In[ ]:


def showDF(df, limitRows=5, truncate=True):
    if(truncate):
        pandas.set_option('display.max_colwidth', 50)
    else:
        pandas.set_option('display.max_colwidth', -1)
    pandas.set_option('display.max_rows', limitRows)
    display(df.limit(limitRows).toPandas())
    pandas.reset_option('display.max_rows')


# In[ ]:


def uniform_csv(spark, csv_to_process, separator):
    df = spark.read.csv(csv_to_process, header=True, sep=separator)
    df = df.select(['VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance', 'RatecodeID', 'store_and_fwd_flag',
                    'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount'])
    return df


# In[ ]:


def df_format_cassandra(spark, df):
    table_source = spark.read.format('org.apache.spark.sql.cassandra').options(
        table='taxis_bis', keyspace='taxis_ny').load()
    df = df.withColumn("id", monotonically_increasing_id())
    df = df.select([F.col(x).alias(x.lower()) for x in df_taxis.columns])

    return df


def has_column(df, col):
    try:
        df[col]
        return True
    except AnalysisException:
        return False
