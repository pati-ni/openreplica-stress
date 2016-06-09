#!/usr/bin/env bash

source /home/students/cs091747/openreplica/openr-env/bin/activate
function run_test {
    cd $HOME/openreplica/openreplica
    python client.py $*
}

run_test $*