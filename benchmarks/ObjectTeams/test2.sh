#!/bin/bash
# make script fail on first error
set -e
# make SCRIPT_PATH absolute
cd ../../
pushd `dirname $0` > /dev/null
SCRIPT_PATH=`pwd`
popd > /dev/null

if [ "$1" = "1" ]
then
	BENCHMARK="benchmark.TeamBenchmark"
else if [ "$1" = "2" ]
then
	BENCHMARK="benchmark.TeamBenchmark2"
else if [ "$1" = "3" ]
then
	BENCHMARK="benchmark.TeamBenchmark3"
else if [ "$1" = "4" ]
then
	BENCHMARK="benchmark.TeamBenchmark4"
else if [ "$1" = "5" ]
then
	BENCHMARK="benchmark.BankBenchmark"
else if [ "$1" = "6" ]
then
	BENCHMARK="benchmark.BankBenchmark2"
fi

# /bin/bash $SCRIPT_PATH/implementations/build-otj.sh 14 classic 3.8.0

JFR="-XX:StartFlightRecording=filename=bench-classic2.jfr,settings=profile"
WEAV="${SCRIPT_PATH}/benchmarks/ObjectTeams/weavables.txt"

/bin/bash $SCRIPT_PATH/implementations/java14.sh -ea $JFR -Dot.weavable=$WEAV -server -XX:-TieredCompilation -Xmx4G --add-reads jdk.dynalink=ALL-UNNAMED --add-reads java.base=ALL-UNNAMED --add-reads jdk.localedata=ALL-UNNAMED -Xbootclasspath/a:./objectteams/classic-3.8.0/otre_min.jar -javaagent:./objectteams/classic-3.8.0/otredyn_agent.jar -jar ../benchmarks/ObjectTeams/benchmarks-classic-3.8.0.jar $BENCHMARK ${2} ${3}
