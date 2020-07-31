#!/bin/bash
EXEC_PATH=$(dirname "$0")
HP_CMD=hadoop
JAR_PACKAGE=/usr/hadoop-2.8.3/share/hadoop/tools/lib/hadoop-streaming-2.8.3.jar
IN_PATH=/input/plates_data1.txt
OUT_PATH=/output/plates_part
MAP_FILE=${EXEC_PATH}/plate_partition_mapper.py
RED_FILE=${EXEC_PATH}/plate_partition_reducer.py
$HP_CMD fs -rm -r $OUT_PATH
$HP_CMD jar $JAR_PACKAGE \
-D mapred.job.queue.name=bdev \
-D stream.map.input.ignoreKey=true \
-D map.output.key.field.separator=, \
-D num.key.fields.for.partition=1 \
-numReduceTasks 1 \
-input $IN_PATH \
-output $OUT_PATH \
-file $MAP_FILE \
-file $RED_FILE \
-mapper $MAP_FILE \
-reducer $RED_FILE \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
$HP_CMD fs -ls $OUT_PATH