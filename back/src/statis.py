#!/usr/bin/env python
# coding: utf-8

import cassandra
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *
import nbimporter
import pandas
import json
import cleaning as clean
import math
import utils


def mean_col(df, colonne_label):

    mean_df = df.agg(
        round(mean(colonne_label), 2).alias("moyenne_" + colonne_label))
    return mean_df


def count_col(df, colonne_label):
    new_df = df.groupby(
        colonne_label).count()
    return new_df



def traitement_pourcentage(df, colonne_label):

    df_pourcent = count_col(df, colonne_label)
    panda_pourcent = df_pourcent.toPandas()
    panda_json_pourcent = panda_pourcent.to_json(orient='records')
    pourcentage = json.loads(panda_json_pourcent)
    return pourcentage



def traitement_moyenne(df, colonne_label):
    mean_df = mean_col(df, colonne_label)
    panda_mean = mean_df.toPandas()
    mean_json = panda_mean.to_json(orient='records')
    moyenne = json.loads(mean_json)
    return moyenne


def element_distinct(df, colonne_label):
    df = df.select(colonne_label).distinct()
    df = df.withColumnRenamed(colonne_label, colonne_label + '_distinct')
    panda = df.toPandas()
    json_dict = panda.to_dict(orient='list')
    return json_dict


def get_metric(df, choix):
    before = df.count()
    after = 0
    if (choix == 'nan'):
        after = df.dropna().count()
    elif (choix == 'duplicate'):
        after = df.dropDuplicates().count()

    return before - after


def group_class(to_groupe, name, interval):
    class_below = {name: '<=0', 'count': 0}
    class_one = {name: '0-' + str(interval), 'count': 0}
    class_two = {name: str(interval) + '-' + str(interval * 2), 'count': 0}
    class_three = {
        name: str(interval * 2) + '-' + str(interval * 3),
        'count': 0
    }
    class_four = {
        name: str(interval * 3) + '-' + str(interval * 4),
        'count': 0
    }
    class_five = {
        name: str(interval * 4) + '-' + str(interval * 5),
        'count': 0
    }
    class_six = {name: '>' + str(interval * 5), 'count': 0}
    merge = []

    for item in to_groupe:

        if (item[name] <= 0):
            class_below['count'] += item['count']
        elif ((item[name] > 0) & (item[name] < interval)):
            class_one['count'] += item['count']
        elif ((item[name] > interval) & (item[name] < interval * 2)):
            class_two['count'] += item['count']
        elif ((item[name] > 2 * interval) & (item[name] < 3 * interval)):
            class_three['count'] += item['count']
        elif ((item[name] > interval * 3) & (item[name] < interval * 4)):
            class_four['count'] += item['count']
        elif ((item[name] > interval * 4) & (item[name] < interval * 5)):
            class_five['count'] += item['count']
        elif (item[name] > interval * 5):
            class_six['count'] += item['count']

    merge.append(class_below)
    merge.append(class_one)
    merge.append(class_two)
    merge.append(class_three)
    merge.append(class_four)
    merge.append(class_five)
    merge.append(class_six)

    return merge


# recuperer les statistiques sans nettoyage
def get_stats(df_metric, df_filter, profil_count, profil_filtered_count,
              count_taxis):

    json_metric = [{
        'total': profil_count,
        'nan': math.fabs(count_taxis - profil_count),
        'total_filtered': profil_filtered_count,
        'total_taxis': count_taxis
    }]

    count_depart = traitement_pourcentage(df_filter, 'zone_depart')

    count_arrivee = traitement_pourcentage(df_filter, 'zone_arrivee')

    moyenne_total_amount = traitement_moyenne(df_filter, 'total_amount')

    moyenne_trip_distance = traitement_moyenne(df_filter, 'trip_distance')

    count_paiement = []
    moyenne_passenger_count = []
    tip = []
    fare = []

    if ('payment_type' in df_filter.columns):
        count_paiement = traitement_pourcentage(df_filter, 'payment_type')

    if ('passenger_count' in df_filter.columns):
        moyenne_passenger_count = traitement_moyenne(df_filter,
                                                     'passenger_count')
    #

    if ('fare_amount' in df_filter.columns):
        fare = traitement_pourcentage(df_filter, 'fare_amount')

        fare = group_class(fare, "fare_amount", 25)

    if ('tip_amount' in df_filter.columns):
        tip = traitement_pourcentage(df_filter, 'tip_amount')
        tip = group_class(tip, "tip_amount", 5)

    moyenne = [
        *moyenne_total_amount, *moyenne_trip_distance, *moyenne_passenger_count
    ]

    json_values = json.dumps({
        'zone_depart_distinct': count_depart,
        'zone_arrivee_distinct': count_arrivee,
        'paiement_type_distinct': count_paiement,
        'fare_amount_distinct': fare,
        'tip_amount_distinct': tip,
        'moyenne': moyenne,
        'metrique': json_metric
    })

    return json_values


def traitement_statistiques(df_metric, df_filter, voyageur_count,
                            profil_filtered_count, count_taxis):

    df_filter = df_filter.dropna()

    json_values = get_stats(df_metric, df_filter, voyageur_count,
                            profil_filtered_count, count_taxis)

    return json_values
