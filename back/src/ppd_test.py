
import unittest
import nbimporter
from unittest_pyspark import as_list, get_spark

from pyspark.sql.types import *
from pyspark.sql import functions as F
import sys

# sys.path.append("../src'")

# print(sys.path)
# from src.cleaning import *


import cleaning
import statis
import voyageur

'''
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import *

@pytest.fixture(scope="session")
def spark_context(request):
    """ fixture for creating a spark context
    Args:
        request: pytest.FixtureRequest object
    """
    conf = (SparkConf().setMaster("local[2]").setAppName("pytest-pyspark-local-testing"))
    spark = SparkContext(conf=conf)
    request.addfinalizer(lambda: spark.stop())

    return spark
'''

    
class cleaning_test(unittest.TestCase): 
    def setUp(self):
          self.spark = get_spark()

    def test_delete_null_data (self):
 
        # GIVEN : préparer les données du test
        l = [(0.0, 6.984555120853725, 2,'Manhattan','Manhattan'), (20.8, 6.984555120853725, 2,'Manhattan','Manhattan'), (20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),(20.8, 6.984555120853725, 2,'Manhattan','Manhattan'),]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'trip_distance', 'vendorid', 'zone_depart', 'zone_arrivee'])
          
        # WHEN : exécuter la fonction testée
        clean_df = cleaning.delete_null_data(df_test,'total_amount')
        
        # THEN : vérifier les résultats
        #self.assertEqual(clean_df.where('total_amount == 0.0').count(), 0)
        self.assertTrue(clean_df.where('total_amount == 0.0').count() == 0)
        self.assertNotEqual(0, clean_df.count())

  
    def test_convert(self):
        
        #given
        l = [('6.984555120853725', 'Manhattan'), ('8.984555120853725', 'Queens'),]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])
       
        #when
        convert_df = cleaning.convert(df_test, 'total_amount', DoubleType())
        #then
        self.assertFalse(df_test.schema["total_amount"].dataType == DoubleType())
        self.assertTrue(convert_df.schema["total_amount"].dataType == DoubleType())
        
  
    def test_convert_date(self):
       #GIVEN
       # MM/dd/yyyy hh:mm:ss aa   
        
        l = [('06/21/2018 01:53:11 PM', 'Manhattan'),]
        df = self.spark.createDataFrame(l, ['time', 'city'])

        date_df = cleaning.convert_date(df, 'time')
        
        self.assertTrue(date_df.schema["TIME_time"].dataType == TimestampType())
            
        
    def test_delete_above(self):

        l = [(6.984555120853725, 'Manhattan'), (8.984555120853725, 'Queens'), (12.984555120853725, 'Queens'), (2.984555120853725, 'Queens')]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])
        
        l_res = [(6.984555120853725, 'Manhattan'), (8.984555120853725, 'Queens'), (2.984555120853725, 'Queens')]
        df_res = self.spark.createDataFrame(l_res, ['total_amount', 'zone_depart'])
        
        new_df = cleaning.delete_above(df_test, 'total_amount', '10')
        
        diff = df_res.subtract(new_df)
        
        self.assertTrue(diff.count()==0)
        self.assertTrue(new_df.where('total_amount > 10').count() == 0)
        
        
        
    def test_delete_under(self):
    
        l = [(6.984555120853725, 'Manhattan'), (8.984555120853725, 'Queens'), (12.984555120853725, 'Queens'), (2.984555120853725, 'Queens')]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])
        
        l_res = [(12.984555120853725, 'Queens')]
        df_res = self.spark.createDataFrame(l_res, ['total_amount', 'zone_depart'])
        
        new_df = cleaning.delete_under(df_test, 'total_amount', '10')

        diff = df_res.subtract(new_df)
        
        self.assertTrue(diff.count()==0)
        self.assertTrue(new_df.where('total_amount < 10').count() == 0)
        
        
    def test_delete_between(self):
        
        l = [(6.984555120853725, 'Manhattan'), (8.984555120853725, 'Queens'), (12.984555120853725, 'Queens'), (2.984555120853725, 'Queens')]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])
        
        new_df = cleaning.delete_between(df_test, 'total_amount','1' ,'10')
        
        self.assertTrue(new_df.where('total_amount > 10').count() == 0)
        self.assertTrue(new_df.where('total_amount < 1').count() == 0)

    
    def test_mile_to_km(self):
        l = [(1, 'Manhattan')]
        df_test = self.spark.createDataFrame(l, ['trip_distance', 'zone_depart'])

        df = cleaning.mile_to_km(df_test)
        
        self.assertEqual(df.select('trip_distance').collect()[0].trip_distance, 1/0.621371)
        self.assertFalse(df.select('trip_distance').collect()[0].trip_distance == 12)


class statis_test(unittest.TestCase): 

    def setUp(self):
        self.spark = get_spark()



    def test_mean_col(self):
        
        l = [(2, 'Manhattan'), (4, 'Manhattan')]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])

        
        mean = statis.mean_col(df_test, 'total_amount')
        
        self.assertEqual(3, mean.select('moyenne_total_amount').collect()[0].moyenne_total_amount) 


    def test_count_col(self):
        
        l = [(2, 'Manhattan'), (4, 'Manhattan'), (2, 'Queens'), (3, 'Queens')]
        df_test = self.spark.createDataFrame(l, ['total_amount', 'zone_depart'])
    
        nb_zone = statis.count_col(df_test, 'zone_depart')
        nb_total_amount = statis.count_col(df_test, 'total_amount')

        self.assertEqual(2, nb_zone.count()) 
        self.assertTrue(nb_total_amount.count() == 3)



unittest.main()
