#!/bin/bash
SCRIPT_PATH=`dirname $0`
source $SCRIPT_PATH/config.inc
exec $JAVA14_HOME/bin/java "$@"
