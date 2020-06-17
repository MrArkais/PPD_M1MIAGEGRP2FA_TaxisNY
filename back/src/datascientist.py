
from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import nbimporter
import cleaning as clean


def convert(df):

    df = clean.convert(df, 'dolocationid', IntegerType())
    df = clean.convert(df, 'extra', DoubleType())
    df = clean.convert(df, 'fare_amount', DoubleType())
    df = clean.convert(df, 'improvement_surcharge', DoubleType())
    df = clean.convert(df, 'mta_tax', DoubleType())
    df = clean.convert(df, 'passenger_count', IntegerType())
    df = clean.convert(df, 'payment_type', IntegerType())
    df = clean.convert(df, 'pulocationid', IntegerType())

    df = clean.convert(df, 'ratecodeid', IntegerType())
    df = clean.convert(df, 'tip_amount', DoubleType())
    df = clean.convert(df, 'tolls_amount', DoubleType())
    df = clean.convert(df, 'trip_distance', DoubleType())

    df = clean.convert(df, 'total_amount', DoubleType())
    df = clean.convert(df, 'vendorid', IntegerType())

    return df


def get_zone(df_taxis, df_zones):

    df_taxis = df_taxis.join(
        df_zones, df_zones['locationid'] == df_taxis['pulocationid'], how='full')
    df_taxis = df_taxis.select(['dolocationid', 'extra', 'fare_amount', 'improvement_surcharge', 'mta_tax', 'passenger_count', 'payment_type',
                                'pulocationid', 'ratecodeid', 'tip_amount', 'tolls_amount', 'trip_distance', 'total_amount', 'vendorid', 'borough'])
    df_taxis = df_taxis.withColumnRenamed("borough", "zone_depart")

    df_taxis = df_taxis.join(
        df_zones, df_zones['locationid'] == df_taxis['dolocationid'], how='full')
    df_taxis = df_taxis.select(['dolocationid', 'extra', 'fare_amount', 'improvement_surcharge', 'mta_tax', 'passenger_count', 'payment_type',
                                'pulocationid', 'ratecodeid', 'tip_amount', 'tolls_amount', 'trip_distance', 'total_amount', 'vendorid', "zone_depart", 'borough'])
    df_taxis = df_taxis.withColumnRenamed("borough", "zone_arrivee")

    return df_taxis
