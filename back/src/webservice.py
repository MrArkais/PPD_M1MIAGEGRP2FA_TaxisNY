#!/usr/bin/env python
# coding: utf-8

# <h2>Imports des modules</h2>
# In[ ]:
import cassandra
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from pyspark import StorageLevel
import nbimporter
import pandas

# <h2>Imports des autres classes</h2>

import utils as utls
import cleaning as clean
import insertion as insert
import voyageur as voyageur
import traitement as traitement
import statis as stats

# <h2>Imports des modules WebService</h2>

import uuid
import os
import re
from waitress import serve
import json
from flask import Flask, json, request, jsonify, Response
import time
from flask_cors import CORS
import sys

api = Flask(__name__)
CORS(api)


cluster = input("Voulez vous utiliser le cluster Spark ? (O/N) : ")

while ((cluster != 'O') and (cluster != 'N')):
    print(f'{cluster} est une saisie incorrecte !')
    cluster = input("Voulez vous utiliser le cluster Spark ? (O/N) : ")

if (cluster == "N"):
    spark = SparkSession.builder.appName("Cassandra Import").config(
        "spark.jars.packages",
        "com.datastax.spark:spark-cassandra-connector_2.11:2.3.3").config(
            "spark.cassandra.connection.host",
            "127.0.0.1").config("spark.cassandra.connection.port",
                                "9042").getOrCreate()


if (cluster == "O"):
    spark = SparkSession.builder.appName("Cassandra Import").config(
        "spark.jars.packages",
        "com.datastax.spark:spark-cassandra-connector_2.11:2.3.3").config(
            "spark.cassandra.connection.host",
            "25.138.28.179").config("spark.cassandra.connection.port", "9042").config("spark.executor.memory", "6g").master("spark://25.138.28.179:7077").getOrCreate()


keyspace = input("Entrez le nom du Keyspace Cassandra à utiliser : ")

init = input("Voulez vous initialiser la base cassandra ? (O/N) ")

if (init == "O"):
    insert.init_database()
    insert.insert_database()
    insert.create_csv(spark, "xaa.csv", ";", keyspace)


start = time.time()

df_taxis = spark.read.format('org.apache.spark.sql.cassandra').options(
    table='taxis', keyspace=keyspace).load()
df_zones = spark.read.format('org.apache.spark.sql.cassandra').options(
    table='zones', keyspace=keyspace).load()


df_taxis_ = df_taxis.persist(StorageLevel.MEMORY_AND_DISK)
df_zones = df_zones.persist(StorageLevel.MEMORY_AND_DISK)
count_taxis = df_taxis.count()
count_zones = df_zones.count()
print(count_taxis)
print(count_zones)


voyageur = traitement.traitement_voyageur(df_taxis, df_zones)
voyageur = voyageur.persist(StorageLevel.MEMORY_AND_DISK)

count_voyageurs = voyageur.count()
print("VOYAGEUR " + str(count_voyageurs))


datascientist = traitement.traitement_datascientist(df_taxis, df_zones)
datascientist = datascientist.persist(StorageLevel.MEMORY_AND_DISK)
count_datascientist = datascientist.count()
print("DATASCIENTIST " + str(count_datascientist))

end = time.time()

print(end - start, " secondes écoulées pour initialiser l'application, contenant : ",
      count_taxis + count_zones, f" lignes dans le keyspace {keyspace} ")


@api.route('/')
def get_uuid():
    return str(uuid.uuid4())


@api.after_request
def add_hostname_header(response):
    env_host = str(os.environ.get('HOSTNAME'))
    hostname = re.findall('[a-z]{3}-\d$', env_host)
    if hostname:
        response.headers["SP-LOCATION"] = hostname
    return response


@api.route('/init', methods=['GET'])
def elements_distincts():

    zone_dep = stats.element_distinct(df_zones, 'borough')
    zone_arr = stats.element_distinct(df_zones, 'borough')
    vendorid = stats.element_distinct(df_taxis, 'vendorid')
    values = []
    values.extend([zone_dep, zone_arr, vendorid])

    json_values = json.dumps(values)

    return Response(json_values, mimetype='application/json')

# In[ ]:


@api.route('/voyageur', methods=['POST'])
def filter_for_voyageur():
    start = time.time()
    # Affichage des infos clients
    print("Adresse : ", request.remote_addr)

    filters = request.get_json()
    print("Filtres recus : ", filters)
    before_filter = count_voyageurs
    filtered_datas = traitement.to_filter(voyageur, filters)
    after_filter = filtered_datas.count()

    # traitement_statistiques renvoient deja un str/json
    statistiques = stats.traitement_statistiques(
        voyageur, filtered_datas, before_filter, after_filter, count_taxis)
    end = time.time()

    print(end - start, " secondes écoulées")
    return Response(statistiques, mimetype='application/json')


@api.route('/datascientist', methods=['POST'])
def filter_for_scientists():
    start = time.time()
    filters = request.get_json()
    print("Filtres recus : ", filters)
    before_filter = count_datascientist
    filtered_datas = traitement.to_filter(datascientist, filters)
    after_filter = filtered_datas.count()

    # traitement_statistiques renvoient deja un str/json
    statistiques = stats.get_stats(
        datascientist, filtered_datas, before_filter, after_filter, count_taxis)
    end = time.time()

    print(end - start, " secondes écoulées")
    return Response(statistiques, mimetype='application/json')


if __name__ == '__main__':
    serve(api, listen='localhost:8070')
