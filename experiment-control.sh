#!/usr/bin/env bash

LOGGER_NODE=node09
LOGGER_CONF=$HOME/zoo_log.cfg
LOGGER_DATADIR=/media/localhd/cs091747/zk-logger/data
LOGGER_DATALOGDIR=/var/tmp/cs091747/zk-logger
ZK=$HOME/zookeeper/server/zookeeper
case $1 in
start)
    ssh $LOGGER_NODE "bash -c \"\
                    rm -rf $LOGGER_DATADIR ;\
                    rm -rf $LOGGER_DATALOGDIR;\
                    rm -rf /var/tmp/cs091747/zookeeper-logger;\
                    mkdir -p $LOGGER_DATADIR ;\
                    mkdir -p /var/tmp/cs091747/zookeeper-logger;\
                    mkdir -p $LOGGER_DATALOGDIR ;\
                    echo 1 > $LOGGER_DATALOGDIR/myid;\
                            cp  $LOGGER_CONF /var/tmp/cs091747/zookeeper/;\
                    $ZK start $LOGGER_CONF\""
;;
stop)
            ssh $LOGGER_NODE "bash -c \"\
                    $ZK $3 $LOGGER_CONF;
                rm -rf $LOGGER_DATADIR;\
                rm -rf $LOGGER_DATALOGDIR\""

;;
*)
    echo "Unknown Command $1"
;;
esac