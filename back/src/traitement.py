#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import cassandra
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
import nbimporter
import json

# In[ ]:

import utils as utls
import cleaning as clean
import insertion as insert
import voyageur as voyageur
import traitement as traitement
import statis as stats
import datascientist as datascientist

# In[ ]:


def traitement_voyageur(df_taxis, df_zones):
    voyageur_datas = voyageur.get_datas_profile_voyageur(df_taxis)
    voyageur_datas = voyageur.convert(voyageur_datas)
    voyageur_datas = voyageur.get_zone(voyageur_datas, df_zones)
    voyageur_datas = clean.mile_to_km(voyageur_datas)
    return voyageur_datas


# In[ ]:


def traitement_datascientist(df_taxis, df_zones):

    data_scientist = datascientist.convert(df_taxis)
    data_scientist = datascientist.get_zone(data_scientist, df_zones)
    data_scientist = clean.mile_to_km(data_scientist)

    return data_scientist


def traitement_entreprise(df_taxis, df_zones):
    entreprise_datas = entreprise.get_datas_profile_entreprise_taxis(df_taxis)
    entreprise_datas = entreprise.convert(entreprise_datas)
    entreprise_datas = entreprise.to_euros(entreprise_datas)
    entreprise_datas = entreprise.get_zone(entreprise_datas, df_zones)
    return entreprise_datas


# In[ ]:


def to_filter(df, filters):

    
    # min max :
    if (("total_amount_min" in filters) & ("total_amount_max" in filters)):
        filtered_data = clean.delete_between(df, "total_amount",
                                             str(filters['total_amount_min']),
                                             str(filters['total_amount_max']))

    if (('trip_distance_min' in filters) & ('trip_distance_max' in filters)):
        filtered_data = clean.delete_between(filtered_data, "trip_distance",
                                             str(filters['trip_distance_min']),
                                             str(filters['trip_distance_max']))

    if ('vendorid' in filters):
        filtered_data = filtered_data.where(
            filtered_data.vendorid.isin(filters['vendorid']))

    if ('zone_depart' in filters):
        filtered_data = filtered_data.where(
            filtered_data.zone_depart.isin(filters["zone_depart"]))

    if ('zone_arrivee' in filters):
        filtered_data = filtered_data.where(
            filtered_data.zone_arrivee.isin(filters["zone_arrivee"]))

    if (('extra_min' in filters) & ('extra_max' in filters)):
        filtered_data = clean.delete_between(df, "extra",
                                             str(filters['extra_min']),
                                             str(filters['extra_max']))

    if (('fare_amount_min' in filters) & ('fare_amount_max' in filters)):
        filtered_data = clean.delete_between(df, "fare_amount",
                                             str(filters['fare_amount_min']),
                                             str(filters['fare_amount_max']))

    if (('improvement_surcharge_min' in filters) &
        ('improvement_surcharge_max' in filters)):
        filtered_data = clean.delete_between(
            df, "improvement_surcharge",
            str(filters['improvement_surcharge_min']),
            str(filters['improvement_surcharge_max']))

    if (('mta_tax_min' in filters) & ('mta_tax_max' in filters)):
        filtered_data = clean.delete_between(df, "mta_tax",
                                             str(filters['mta_tax_min']),
                                             str(filters['mta_tax_max']))

    if (('passenger_count_min' in filters) &
        ('passenger_count_max' in filters)):
        filtered_data = clean.delete_between(
            df, "passenger_count", str(filters['passenger_count_min']),
            str(filters['passenger_count_max']))

    if (('tip_amount_min' in filters) & ('tip_amount_max' in filters)):
        filtered_data = clean.delete_between(df, "tip_amount",
                                             str(filters['tip_amount_min']),
                                             str(filters['tip_amount_max']))

    if (('tolls_amount_min' in filters) & ('tolls_amount_max' in filters)):
        filtered_data = clean.delete_between(df, "tolls_amount",
                                             str(filters['tolls_amount_min']),
                                             str(filters['tolls_amount_max']))

    if ('ratecodeid' in filters):
        filtered_data = filtered_data.where(
            filtered_data.vendorid.isin(filters['ratecodeid']))

    if ('payment_type' in filters):
        filtered_data = filtered_data.where(
            filtered_data.vendorid.isin(filters['payment_type']))

    return filtered_data

