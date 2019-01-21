from lib.hdfs import Hdfs
from lib.spark import SparkAutomate
from lib.hive import HiveAutomate
from lib.oozie import OozieAutomate
from lib.data import Dataset
from lib.util import Util
from conf.config import *
import subprocess
import time

if __name__ == '__main__':
    util = Util()
    util.get_cluster_details()
    hdfs = Hdfs() 
    
    start_time = time.time()
    
    try:
        print("Setting up the datasets .. ")
        data = Dataset( url_list, util)
        data.automate()
    except Exception as e:
        print("Failed to set up the datasets !")
        print("Following exception has occured " + str(e))
    else :
        try : 
            print("Running spark application..")
            spark = SparkAutomate(spark_dir_list, util, hdfs)
            spark.automate()
        except Exception as e:
            print("Failed to run spark application !")
            print("Following exception has occured " + str(e))
        try:
            print("Running hive queries .. ")
            hive = HiveAutomate( hive_dir_list, util, hdfs)
            hive.automate()
        except Exception as e: 
            print("Failed to run hive queries !")
            print("Following exception has occured " + str(e))
        else:
            try:
                print("Running oozie workflow...")
                oozie = OozieAutomate( oozie_dir_list, hdfs, util)
                oozie.automate()
            except Exception as e:
                print("Failed to run oozie workflow !")
                print("Following exception has occured " + str(e))
    print("----- Total time taken for automation : %s seconds -----" % (time.time() - start_time))
    
