FROM apache/airflow:2.7.3

ENV JDK_TAR_NAME jdk.tar.gz



USER airflow
# Install dependencies from requirements.txt
# The relative path specified in the COPY instruction is relative to the build context
# Not the location of the Dockerfile
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt
ADD ${JDK_TAR_NAME} .

ENV JAVA_HOME=/opt/openlogic-openjdk-8u392-b08-linux-x64
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin