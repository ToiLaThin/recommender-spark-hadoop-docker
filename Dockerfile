FROM ubuntu:20.04
# FROM alpine:3.14
# alpine is minial docker image based on alpine linux
#base ubuntu image then we extend
ENV PYTHON_VERSION=3.9
ENV JDK_VERSION=8u392-b08
ENV HADOOP_VERSION=3.3.4
ENV PIG_VERSION=0.17.0
ENV MAHOUT_VERSION=0.13.0
ENV DERBY_VERSION=10.14.2.0
ENV HIVE_VERSION=3.1.3
ENV SPARK_VERSION=3.5.0

# ENV JDK_TAR_NAME jdk.tar.gz
# ENV HADOOP_TAR_NAME hadoop.tar.gz
# ENV PIG_TAR_NAME pig-0.17.0.tar.gz
# ENV MAHOUT_TAR_NAME apache-mahout-distribution-0.13.0.tar.gz
# ENV DERBY_TAR_NAME db-derby-10.14.2.0-bin.tar.gz
# ENV HIVE_TAR_NAME apache-hive-3.1.3-bin.tar.gz
# ENV SPARK_TAR_NAME spark-3.5.0-bin-hadoop3.tgz
#set environment variables of what we need

#update & install dependencies and python
WORKDIR /opt
#set work dir for add, copy, run, and entrypoint, cmd

ENV DEBIAN_FRONTEND=noninteractive 
# this work to avoid prompt in the middle of the installation in docker
RUN apt update && apt install -y arp-scan python3 && \
    apt install -y wget
    
RUN apt install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install python${PYTHON_VERSION} -y && \
    apt clean

RUN wget https://builds.openlogic.com/downloadJDK/openlogic-openjdk/${JDK_VERSION}/openlogic-openjdk-${JDK_VERSION}-linux-x64.tar.gz && \
    tar -xzf openlogic-openjdk-${JDK_VERSION}-linux-x64.tar.gz && \
    #will untar it to openlogic-openjdk-8u392-b08-linux-x64
    rm openlogic-openjdk-${JDK_VERSION}-linux-x64.tar.gz
    
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    #will untar it to hadoop-3.3.4
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

RUN wget https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz && \
    #will untar it to pig-0.17.0
    tar -xzf pig-${PIG_VERSION}.tar.gz && \
    rm pig-${PIG_VERSION}.tar.gz

RUN wget https://archive.apache.org/dist/mahout/${MAHOUT_VERSION}/apache-mahout-distribution-${MAHOUT_VERSION}.tar.gz && \
    #will untar it to apache-mahout-distribution-0.13.0
    tar -xzf apache-mahout-distribution-${MAHOUT_VERSION}.tar.gz && \
    rm apache-mahout-distribution-${MAHOUT_VERSION}.tar.gz

RUN wget https://archive.apache.org/dist/db/derby/db-derby-${DERBY_VERSION}/db-derby-${DERBY_VERSION}-bin.tar.gz && \
    #will untar it to db-derby-10.14.2.0-bin, let it there for the extend image to config it
    tar -xzf db-derby-${DERBY_VERSION}-bin.tar.gz && \
    rm db-derby-${DERBY_VERSION}-bin.tar.gz

RUN wget https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    #will untar it to apache-hive-3.1.3-bin
    tar -xzf apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    rm apache-hive-${HIVE_VERSION}-bin.tar.gz

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    #will untar it to spark-3.5.0-bin-hadoop3
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# copy assets from local machine to container image
# ADD ./assets/${JDK_TAR_NAME} .
# ADD ./assets/${HADOOP_TAR_NAME} .
# will untar it to pig-0.17.0
# ADD ./assets/${PIG_TAR_NAME} . 
# will untar it to apache-mahout-distribution-0.13.0
# ADD ./assets/${MAHOUT_TAR_NAME} . 
# will untar it to db-derby-10.14.2.0-bin, let it there for the extend image to config it
# ADD ./assets/${DERBY_TAR_NAME} .
# will untar it to apache-hive-3.1.3-bin
# ADD ./assets/${HIVE_TAR_NAME} .
# will untar it to spark-3.5.0-bin-hadoop3
# ADD ./assets/${SPARK_TAR_NAME} .
# add command will untar to add java to the path

# open assets folder , run tar to see the name after untar TAR -XZVF: untar, extract, verbose, file
ENV JAVA_HOME=/opt/openlogic-openjdk-8u392-b08-linux-x64
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin
#this keep the path, add java home to the path, and add java home bin to the path
ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HADOOP_STREAMING_JAR=${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar
ENV PATH=$PATH:$HADOOP_HOME:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

ENV PIG_HOME=/opt/pig-0.17.0
ENV PATH=$PATH:$PIG_HOME/bin

ENV MAHOUT_HOME=/opt/apache-mahout-distribution-0.13.0
ENV PATH=$PATH:$MAHOUT_HOME/bin

ENV DERBY_HOME=/opt/db-derby-10.14.2.0-bin
ENV DERBY_LIB=$DERBY_HOME/lib
ENV PATH=$PATH:$DERBY_HOME/bin

ENV HIVE_HOME=/opt/apache-hive-3.1.3-bin
ENV HADOOP_USER_CLASSPATH_FIRST=true
ENV HIVE_LIB=$HIVE_HOME/lib
ENV PATH=$PATH:$HIVE_HOME/bin

ENV SPARK_HOME=/opt/spark-3.5.0-bin-hadoop3
ENV SPARK_MASTER=spark://spark-master:7077
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_WEBUI_PORT=8082
ENV PYSPARK_PYTHON=python3
# this will stop spark from running in the background as a daemon, docker container will not stop
ENV SPARK_NO_DAEMONIZE=true
# ???
ENV PYTHONPATH=$PYTHONPATH:$SPARK_HOME/python/
# some command to start spark master and worker node is in sbin folder so we need to add it to the path
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Set user for HDFS and Yarn (for production probably not smart to put root)
# This is to run start-yarn or start-dfs
ENV HDFS_NAMENODE_USER="root"
ENV HDFS_DATANODE_USER="root"
ENV HDFS_SECONDARYNAMENODE_USER="root"
ENV YARN_RESOURCEMANAGER_USER="root"
ENV YARN_NODEMANAGER_USER="root"


ADD ./config_files/core-site.xml ${HADOOP_HOME}/etc/hadoop/
ADD ./config_files/hadoop-env.sh ${HADOOP_HOME}/etc/hadoop/
ADD ./config_files/yarn-site.xml ${HADOOP_HOME}/etc/hadoop/
ADD ./config_files/mapred-site.xml ${HADOOP_HOME}/etc/hadoop/

# config file for spark
ADD ./config_files/spark-defaults.conf ${SPARK_HOME}/conf/
#We don’t run this image directly as a container, so no need to add a CMD or ENTRYPOINT instruction.
