# 大規模データ処理法

### 20190422

## Cloud Computing: X As A Service
- Saas: Software As A Service
    - Gmali
- PaaS: Platform As A Service
    - Google App Engine, Azure
- Iaas: Infrastructure As A Service
    - Amazon EC2

- Software platform of Google... Google File System, BigTable, MapReduce
- Hadoop System (Google Clone) ... Hadoop Distributed File System (HDFS), hBase, MapReduce

## MapReduce

- Retrieving is the biggest problem when using big data
- →  distribute the  data itself, distribute them, process them paralely

## HDFS

- NameNode... holds metadata and user information
- DataNode... Data
- When user access data, NameNode is first accessed and then the data in DataNode is read/written.

## MapReduce
1. Split
2. Map
3. Combine
4. Shuffle... not random shuffle, but collecting same type of data
5. Sort
6. Reduce










