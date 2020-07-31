#!/bin/bash
EXEC_PATH=$(dirname "$0")
HP_CMD=hadoop
JAR_PACKAGE=/usr/hadoop-2.8.3/share/hadoop/tools/lib/hadoop-streaming-2.8.3.jar
IN_PATH=/input/plates_data2.txt
OUT_PATH=/output/plates_secsort
MAP_FILE=${EXEC_PATH}/plate_secsort_mapper.py
RED_FILE=${EXEC_PATH}/plate_secsort_reducer.py
$HP_CMD fs -rm -r $OUT_PATH
$HP_CMD jar $JAR_PACKAGE \
-D mapred.job.queue.name=bdev \
-D stream.map.input.ignoreKey=true \
-D stream.map.output.field.separator=, \
-D stream.num.map.output.key.fields=3 \
-D map.output.key.field.separator=, \
-D num.key.fields.for.partition=1 \
-D mapred.output.key.comparator.class=\
org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapred.text.key.comparator.options=-k3,3nr \
-numReduceTasks 5 \
-input $IN_PATH \
-output $OUT_PATH \
-file $MAP_FILE \
-file $RED_FILE \
-mapper $MAP_FILE \
-reducer $RED_FILE \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
$HP_CMD fs -ls $OUT_PATH