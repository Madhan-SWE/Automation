from conf.config import *
import os
class HiveAutomate:
    def __init__(self, hive_dir_list, util, hdfs) :
        self.dir_list = hive_dir_list
        self.util = util
        self.hdfs = hdfs

    def create_hdfs_directories(self):
        print("creating hdfs directories for hive")
        for directory in self.dir_list:
            self.hdfs.make_dir(directory, self.util)

        self.hdfs.own_dir(self.dir_list[0], self.util)

    def convert_to_orc(self):
        print("converting dataset to orc format")
        dataset_year = 2013
        if not os.path.exists(HIVE_TARGET):
            os.makedirs(HIVE_TARGET)

        for year in range(dataset_year, 2018):
           cmd = "python src/rsrch_process.py "+LOCAL_DATASET_PATH+"/OP_DTL_RSRCH_PGYR"+str(year)+DATASET_SUFFIX+".csv "+HIVE_TARGET+"/"+str(year)+".csv "+str(year)
           self.util.run_call(cmd, shell=True)

    def push_data_to_hdfs(self):
         print("pushing data to HDFS")
         for year in range(2013, 2018):
             src = HIVE_TARGET+"/"+str(year)+".csv "
             dest = HDFS_TARGET+"/"+str(year)
             self.hdfs.put_file(src, dest, self.util)

    def load_hive_tables(self):
         print("creating hive tables")
         cmd = "hive -f src/hive_script.sql"
         self.util.run_call(cmd, shell=True)

    def run_query(self):
         print("running hive query")
         cmd = "hive -f src/hive_script.sql"
         self.util.run_call(cmd, shell=True)

    def automate(self):
        self.create_hdfs_directories()
        self.convert_to_orc()
        self.push_data_to_hdfs()
        self.load_hive_tables()
