#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import cassandra
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import monotonically_increasing_id
import nbimporter
import utils as utls
from cassandra.cluster import Cluster


# In[ ]:


def init_database():
    #cluster = Cluster(['25.93.250.31'])
    #    cluster = Cluster(['127.0.0.1'])
    cluster = Cluster(['25.138.28.179'])
    session = cluster.connect()
    # creation d'un keyspace
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS new_taxis
        WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 }; """
                    )
    session.set_keyspace('new_taxis')
    query = "CREATE TABLE IF NOT EXISTS taxis         (id VARCHAR,vendorID VARCHAR, tpep_pickup_datetime VARCHAR, tpep_dropoff_datetime VARCHAR,         Passenger_count VARCHAR, Trip_distance VARCHAR, PULocationID VARCHAR, DOLocationID VARCHAR,         RateCodeID VARCHAR, Store_and_fwd_flag VARCHAR, Payment_type VARCHAR, Fare_amount VARCHAR,        Extra VARCHAR, MTA_tax VARCHAR, Improvement_surcharge VARCHAR, tip_amount VARCHAR,        Tolls_amount VARCHAR, Total_amount VARCHAR,         PRIMARY KEY (id));"
    query2 = "CREATE TABLE IF NOT EXISTS zones         (id VARCHAR,OBJECTID VARCHAR, Shape_Leng VARCHAR, the_geom VARCHAR,         Shape_Area VARCHAR, zone VARCHAR, LocationID VARCHAR, borough VARCHAR, PRIMARY KEY (id));"
    # creation de la table taxis
    session.execute(query)
    session.execute(query2)


def insert_database(keyspace, ):

    spark = SparkSession.builder.appName("Cassandra Import").config(
        "spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.11:2.3.3").getOrCreate()

    df_zones = spark.read.format('org.apache.spark.sql.cassandra').options(
        table='zones', keyspace=keyspace).load()
    csv_zones = spark.read.csv("taxi_zones.csv", header=True, sep=";")
    csv_zones = csv_zones.withColumn("id", monotonically_increasing_id())
    csv_zones = csv_zones.select(
        [F.col(x).alias(x.lower()) for x in df_zones.columns])

    if (df_zones.count() == 0):
        csv_zones.write.format('org.apache.spark.sql.cassandra').options(
            table='zones', keyspace='new_taxis').save(mode="append")


def create_csv(spark, csv, separator, keyspace):
    df_unformat = utls.uniform_csv(spark, csv, separator)
    df_format = utls.df_format_cassandra(spark, df_unformat)

    df_zones = spark.read.format('org.apache.spark.sql.cassandra').options(
        table='zones', keyspace=keyspace).load()
    csv_zones = spark.read.csv("taxi_zones.csv", header=True, sep=";")
    csv_zones = csv_zones.withColumn("id", monotonically_increasing_id())
    csv_zones = csv_zones.select(
        [F.col(x).alias(x.lower()) for x in df_zones.columns])

    df_format.coalesce(1).write.option("header", "true").option(
        "sep", ";").mode("overwrite").csv("output/taxis.csv")
    csv_zones.coalesce(1).write.option("header", "true").option(
        "sep", ";").mode("overwrite").csv("output/zones.csv")
