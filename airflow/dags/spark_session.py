import findspark
# findspark.init('/opt/spark-3.5.0-bin-hadoop3')

from pyspark import SparkConf
from pyspark.sql import SparkSession

def init_spark_session():
    master = "spark://spark-master:7077"

    conf = (
        SparkConf()
        .setAppName("Transform")
        .setMaster(master)
        .set("spark.hadoop.hive.metastore.uris", "thrift://hive-server-and-metastore:9080")
        .set("spark.sql.warehouse.dir", "hdfs://namenode-master:9000/user/hive/warehouse")
        .set("spark.memory.offHeap.enabled", "true")
        .set("spark.memory.offHeap.size", "5g")
        .set("spark.executor.memory", "2g")
        .set("hive.exec.dynamic.partition", "true")
        .set("hive.exec.dynamic.partition.mode", "nonstrict")
        .set("spark.sql.session.timeZone", "UTC+7")
        .set("spark.network.timeout", "5000")
        .set("spark.executor.heartbeatInterval", "5000")
        .set("spark.worker.timeout", "5000")
    )

    spark_ss = (
        SparkSession.builder.config(conf=conf)
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark_ss